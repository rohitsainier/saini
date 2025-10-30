"""Model conversion utilities - PyTorch/TensorFlow to ONNX to CoreML."""

import os
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import tempfile
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich import box

console = Console()

class ModelConverter:
    """Convert models between different formats."""
    
    SUPPORTED_FRAMEWORKS = ['pytorch', 'tensorflow', 'keras', 'onnx']
    SUPPORTED_TARGETS = ['onnx', 'coreml']
    
    def __init__(self):
        """Initialize the converter."""
        self.temp_dir = None
        
    def _check_dependencies(self, framework: str, target: str) -> bool:
        """Check if required dependencies are installed."""
        required_packages = []
        
        if framework == 'pytorch':
            required_packages.extend(['torch', 'onnx'])
        elif framework in ['tensorflow', 'keras']:
            required_packages.extend(['tensorflow', 'tf2onnx', 'onnx'])
        elif framework == 'onnx':
            required_packages.append('onnx')
            
        if target == 'coreml':
            required_packages.append('coremltools')
        
        missing = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            console.print(f"[red]✗ Missing required packages: {', '.join(missing)}[/red]")
            console.print(f"\n[yellow]Install with:[/yellow] pip install {' '.join(missing)}")
            return False
        
        return True
    
    def pytorch_to_onnx(
        self,
        model_path: str,
        output_path: str,
        input_shape: Tuple[int, ...],
        input_names: Optional[List[str]] = None,
        output_names: Optional[List[str]] = None,
        opset_version: int = 11,
        dynamic_axes: Optional[Dict[str, Dict[int, str]]] = None,
        optimize: bool = True
    ) -> bool:
        """
        Convert PyTorch model to ONNX.
        
        Args:
            model_path: Path to PyTorch model (.pt, .pth)
            output_path: Output ONNX file path
            input_shape: Input tensor shape (e.g., (1, 3, 224, 224))
            input_names: Names for input tensors
            output_names: Names for output tensors
            opset_version: ONNX opset version
            dynamic_axes: Dynamic axes for variable input sizes
            optimize: Whether to optimize the ONNX model
        """
        try:
            import torch
            import onnx
            from onnx import optimizer
            
            console.print(f"\n[cyan]🔄 Converting PyTorch → ONNX[/cyan]")
            console.print(f"  Model: {model_path}")
            console.print(f"  Output: {output_path}")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                
                # Load model
                task = progress.add_task("Loading PyTorch model...", total=100)
                model = torch.load(model_path, map_location='cpu')
                
                if isinstance(model, dict) and 'model' in model:
                    model = model['model']
                elif isinstance(model, dict) and 'state_dict' in model:
                    # Need to reconstruct model architecture
                    console.print("[yellow]⚠ State dict found. You need to provide model architecture.[/yellow]")
                    return False
                
                model.eval()
                progress.update(task, advance=30)
                
                # Create dummy input
                progress.update(task, description="Creating dummy input...")
                dummy_input = torch.randn(*input_shape)
                progress.update(task, advance=20)
                
                # Export to ONNX
                progress.update(task, description="Exporting to ONNX...")
                torch.onnx.export(
                    model,
                    dummy_input,
                    output_path,
                    export_params=True,
                    opset_version=opset_version,
                    do_constant_folding=True,
                    input_names=input_names or ['input'],
                    output_names=output_names or ['output'],
                    dynamic_axes=dynamic_axes
                )
                progress.update(task, advance=30)
                
                # Optimize ONNX model
                if optimize:
                    progress.update(task, description="Optimizing ONNX model...")
                    onnx_model = onnx.load(output_path)
                    passes = [
                        'eliminate_deadend',
                        'eliminate_identity',
                        'eliminate_nop_dropout',
                        'eliminate_nop_pad',
                        'eliminate_nop_transpose',
                        'eliminate_unused_initializer',
                        'extract_constant_to_initializer',
                        'fuse_bn_into_conv',
                        'fuse_consecutive_squeezes',
                        'fuse_consecutive_transposes',
                        'fuse_transpose_into_gemm',
                    ]
                    optimized_model = optimizer.optimize(onnx_model, passes)
                    onnx.save(optimized_model, output_path)
                progress.update(task, advance=20)
            
            # Verify
            self._verify_onnx(output_path)
            
            console.print(f"[green]✓ Successfully converted to ONNX[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Conversion failed: {str(e)}[/red]")
            return False
    
    def tensorflow_to_onnx(
        self,
        model_path: str,
        output_path: str,
        opset_version: int = 11,
        optimize: bool = True
    ) -> bool:
        """
        Convert TensorFlow/Keras model to ONNX.
        
        Args:
            model_path: Path to TensorFlow model (.h5, .pb, SavedModel dir)
            output_path: Output ONNX file path
            opset_version: ONNX opset version
            optimize: Whether to optimize the ONNX model
        """
        try:
            import tensorflow as tf
            import tf2onnx
            import onnx
            
            console.print(f"\n[cyan]🔄 Converting TensorFlow → ONNX[/cyan]")
            console.print(f"  Model: {model_path}")
            console.print(f"  Output: {output_path}")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                
                task = progress.add_task("Loading TensorFlow model...", total=100)
                
                # Determine model format and load
                model_path = Path(model_path)
                if model_path.suffix == '.h5':
                    # Keras H5 format
                    model = tf.keras.models.load_model(str(model_path))
                    spec = (tf.TensorSpec(model.input_shape, tf.float32, name="input"),)
                    progress.update(task, advance=30)
                    
                    progress.update(task, description="Converting to ONNX...")
                    onnx_model, _ = tf2onnx.convert.from_keras(
                        model,
                        input_signature=spec,
                        opset=opset_version,
                        output_path=output_path
                    )
                    
                elif model_path.is_dir():
                    # SavedModel format
                    progress.update(task, advance=30)
                    progress.update(task, description="Converting to ONNX...")
                    
                    onnx_model, _ = tf2onnx.convert.from_saved_model(
                        str(model_path),
                        opset=opset_version,
                        output_path=output_path
                    )
                else:
                    console.print("[red]✗ Unsupported TensorFlow model format[/red]")
                    return False
                
                progress.update(task, advance=50)
                
                # Optimize if requested
                if optimize:
                    progress.update(task, description="Optimizing ONNX model...")
                    from onnx import optimizer
                    onnx_model = onnx.load(output_path)
                    passes = optimizer.get_available_passes()
                    optimized_model = optimizer.optimize(onnx_model, passes[:10])
                    onnx.save(optimized_model, output_path)
                
                progress.update(task, advance=20)
            
            # Verify
            self._verify_onnx(output_path)
            
            console.print(f"[green]✓ Successfully converted to ONNX[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Conversion failed: {str(e)}[/red]")
            return False
    
    def onnx_to_coreml(
        self,
        onnx_path: str,
        output_path: str,
        model_name: str = "ConvertedModel",
        minimum_deployment_target: str = "iOS13",
        compute_precision: str = "FLOAT32"
    ) -> bool:
        """
        Convert ONNX model to CoreML.
        
        Args:
            onnx_path: Path to ONNX model
            output_path: Output CoreML file path (.mlmodel)
            model_name: Name for the CoreML model
            minimum_deployment_target: Minimum iOS/macOS version (iOS13, iOS14, iOS15, macOS10_15, etc.)
            compute_precision: Computation precision (FLOAT32, FLOAT16)
        """
        try:
            import coremltools as ct
            from coremltools.converters.onnx import convert as onnx_convert
            
            console.print(f"\n[cyan]🔄 Converting ONNX → CoreML[/cyan]")
            console.print(f"  Model: {onnx_path}")
            console.print(f"  Output: {output_path}")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                
                task = progress.add_task("Loading ONNX model...", total=100)
                progress.update(task, advance=20)
                
                # Parse deployment target
                target_map = {
                    'iOS13': ct.target.iOS13,
                    'iOS14': ct.target.iOS14,
                    'iOS15': ct.target.iOS15,
                    'iOS16': ct.target.iOS16,
                    'macOS10_15': ct.target.macOS10_15,
                    'macOS11': ct.target.macOS11,
                    'macOS12': ct.target.macOS12,
                }
                
                deployment_target = target_map.get(minimum_deployment_target, ct.target.iOS13)
                
                # Parse compute precision
                precision_map = {
                    'FLOAT32': ct.precision.FLOAT32,
                    'FLOAT16': ct.precision.FLOAT16,
                }
                compute_precision_value = precision_map.get(compute_precision, ct.precision.FLOAT32)
                
                progress.update(task, description="Converting to CoreML...")
                
                # Convert
                coreml_model = onnx_convert(
                    model=onnx_path,
                    minimum_ios_deployment_target=deployment_target if 'iOS' in minimum_deployment_target else None,
                    minimum_macos_deployment_target=deployment_target if 'macOS' in minimum_deployment_target else None,
                    compute_precision=compute_precision_value
                )
                
                progress.update(task, advance=60)
                
                # Set metadata
                progress.update(task, description="Setting metadata...")
                coreml_model.author = "Saini Model Converter"
                coreml_model.short_description = f"{model_name} - Converted from ONNX"
                coreml_model.version = "1.0"
                
                progress.update(task, advance=10)
                
                # Save
                progress.update(task, description="Saving CoreML model...")
                coreml_model.save(output_path)
                
                progress.update(task, advance=10)
            
            # Display model info
            self._show_coreml_info(output_path)
            
            console.print(f"[green]✓ Successfully converted to CoreML[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Conversion failed: {str(e)}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return False
    
    def convert(
        self,
        source_model: str,
        output_path: str,
        source_framework: str,
        target_format: str,
        **kwargs
    ) -> bool:
        """
        Universal convert function.
        
        Args:
            source_model: Path to source model
            output_path: Output file path
            source_framework: Source framework (pytorch, tensorflow, keras, onnx)
            target_format: Target format (onnx, coreml)
            **kwargs: Additional arguments for specific converters
        """
        source_framework = source_framework.lower()
        target_format = target_format.lower()
        
        # Validate
        if source_framework not in self.SUPPORTED_FRAMEWORKS:
            console.print(f"[red]✗ Unsupported framework: {source_framework}[/red]")
            console.print(f"[yellow]Supported: {', '.join(self.SUPPORTED_FRAMEWORKS)}[/yellow]")
            return False
        
        if target_format not in self.SUPPORTED_TARGETS:
            console.print(f"[red]✗ Unsupported target: {target_format}[/red]")
            console.print(f"[yellow]Supported: {', '.join(self.SUPPORTED_TARGETS)}[/yellow]")
            return False
        
        # Check dependencies
        if not self._check_dependencies(source_framework, target_format):
            return False
        
        # Convert to ONNX first if needed
        onnx_path = output_path if target_format == 'onnx' else tempfile.mktemp(suffix='.onnx')
        
        try:
            # Step 1: Convert to ONNX
            if source_framework == 'pytorch':
                input_shape = kwargs.get('input_shape')
                if not input_shape:
                    console.print("[red]✗ input_shape required for PyTorch conversion[/red]")
                    console.print("[yellow]Example: --input-shape 1,3,224,224[/yellow]")
                    return False
                
                success = self.pytorch_to_onnx(
                    source_model,
                    onnx_path,
                    input_shape=tuple(map(int, input_shape.split(','))),
                    input_names=kwargs.get('input_names'),
                    output_names=kwargs.get('output_names'),
                    opset_version=kwargs.get('opset_version', 11),
                    optimize=kwargs.get('optimize', True)
                )
                
            elif source_framework in ['tensorflow', 'keras']:
                success = self.tensorflow_to_onnx(
                    source_model,
                    onnx_path,
                    opset_version=kwargs.get('opset_version', 11),
                    optimize=kwargs.get('optimize', True)
                )
                
            elif source_framework == 'onnx':
                onnx_path = source_model
                success = True
            
            else:
                console.print(f"[red]✗ Conversion from {source_framework} not implemented yet[/red]")
                return False
            
            if not success:
                return False
            
            # Step 2: Convert to target format
            if target_format == 'coreml':
                success = self.onnx_to_coreml(
                    onnx_path,
                    output_path,
                    model_name=kwargs.get('model_name', 'ConvertedModel'),
                    minimum_deployment_target=kwargs.get('deployment_target', 'iOS13'),
                    compute_precision=kwargs.get('precision', 'FLOAT32')
                )
                
                # Clean up temp ONNX file
                if onnx_path != output_path and onnx_path != source_model:
                    Path(onnx_path).unlink(missing_ok=True)
                
                return success
            
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Conversion failed: {str(e)}[/red]")
            return False
    
    def _verify_onnx(self, onnx_path: str):
        """Verify and display ONNX model information."""
        try:
            import onnx
            
            model = onnx.load(onnx_path)
            onnx.checker.check_model(model)
            
            # Display model info
            table = Table(title="ONNX Model Info", box=box.ROUNDED)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("IR Version", str(model.ir_version))
            table.add_row("Producer", model.producer_name or "Unknown")
            table.add_row("Opset Version", str(model.opset_import[0].version))
            
            # Inputs
            inputs = []
            for inp in model.graph.input:
                shape = [dim.dim_value for dim in inp.type.tensor_type.shape.dim]
                inputs.append(f"{inp.name}: {shape}")
            table.add_row("Inputs", "\n".join(inputs))
            
            # Outputs
            outputs = []
            for out in model.graph.output:
                shape = [dim.dim_value for dim in out.type.tensor_type.shape.dim]
                outputs.append(f"{out.name}: {shape}")
            table.add_row("Outputs", "\n".join(outputs))
            
            # File size
            size = Path(onnx_path).stat().st_size
            size_mb = size / (1024 * 1024)
            table.add_row("File Size", f"{size_mb:.2f} MB")
            
            console.print()
            console.print(table)
            
        except Exception as e:
            console.print(f"[yellow]⚠ Could not verify ONNX model: {str(e)}[/yellow]")
    
    def _show_coreml_info(self, coreml_path: str):
        """Display CoreML model information."""
        try:
            import coremltools as ct
            
            model = ct.models.MLModel(coreml_path)
            spec = model.get_spec()
            
            table = Table(title="CoreML Model Info", box=box.ROUNDED)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            # Inputs
            inputs = []
            for inp in spec.description.input:
                inputs.append(f"{inp.name}: {inp.type}")
            table.add_row("Inputs", "\n".join(inputs) if inputs else "N/A")
            
            # Outputs
            outputs = []
            for out in spec.description.output:
                outputs.append(f"{out.name}: {out.type}")
            table.add_row("Outputs", "\n".join(outputs) if outputs else "N/A")
            
            # File size
            size = Path(coreml_path).stat().st_size
            size_mb = size / (1024 * 1024)
            table.add_row("File Size", f"{size_mb:.2f} MB")
            
            console.print()
            console.print(table)
            
        except Exception as e:
            console.print(f"[yellow]⚠ Could not read CoreML model info: {str(e)}[/yellow]")
    
    def batch_convert(
        self,
        models_dir: str,
        output_dir: str,
        source_framework: str,
        target_format: str,
        **kwargs
    ):
        """
        Batch convert multiple models.
        
        Args:
            models_dir: Directory containing models
            output_dir: Output directory
            source_framework: Source framework
            target_format: Target format
            **kwargs: Additional conversion arguments
        """
        models_path = Path(models_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find models
        extensions = {
            'pytorch': ['.pt', '.pth'],
            'tensorflow': ['.h5', '.pb'],
            'onnx': ['.onnx']
        }
        
        model_files = []
        for ext in extensions.get(source_framework, []):
            model_files.extend(models_path.glob(f'*{ext}'))
        
        if not model_files:
            console.print(f"[yellow]⚠ No {source_framework} models found in {models_dir}[/yellow]")
            return
        
        console.print(f"\n[cyan]Found {len(model_files)} models to convert[/cyan]\n")
        
        results = {'success': 0, 'failed': 0}
        
        for model_file in model_files:
            output_file = output_path / f"{model_file.stem}.{target_format}"
            
            console.print(f"[dim]Converting: {model_file.name}[/dim]")
            
            success = self.convert(
                str(model_file),
                str(output_file),
                source_framework,
                target_format,
                **kwargs
            )
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
            
            console.print()
        
        # Summary
        console.print(Panel(
            f"[green]✓ {results['success']} succeeded[/green]\n"
            f"[red]✗ {results['failed']} failed[/red]",
            title="Batch Conversion Summary",
            border_style="cyan"
        ))