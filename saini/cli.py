import click
from rich.console import Console

from .tracker import TimeTracker, status_live, status_static
from .config import Config
from .reports import Reports
from .tree import ProjectTree
from . import __version__
from .dashboard import show_dashboard
from .converter import ModelConverter

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__, prog_name="Saini")
def main(ctx):
    """Saini - Developer productivity tools."""
    if ctx.invoked_subcommand is None:
        # Show live status by default
        status_live()


# ============================================================================
# TIME TRACKING COMMANDS
# ============================================================================

@main.command()
@click.argument('description', required=False)
def start(description):
    """Start tracking time."""
    tracker = TimeTracker()
    tracker.start(description)


@main.command()
def stop():
    """Stop current session."""
    tracker = TimeTracker()
    tracker.stop()


@main.command()
@click.argument('description', required=False)
def switch(description):
    """Switch to a new session (stops current)."""
    tracker = TimeTracker()
    tracker.switch(description)


@main.command()
def pause():
    """Pause current session."""
    tracker = TimeTracker()
    tracker.pause()


@main.command()
def resume():
    """Resume paused session."""
    tracker = TimeTracker()
    tracker.resume()

@main.command()
def dashboard():
    """Show live dashboard with all stats."""
    show_dashboard()


@main.command()
@click.option('--live/--static', default=True, help='Show live updating timer')
def status(live):
    """Show current session status with live timer.
    
    Examples:
        saini status           # Live updating timer (default)
        saini status --static  # Static snapshot
    """
    if live:
        status_live()
    else:
        status_static()


# ============================================================================
# CONFIGURATION COMMANDS
# ============================================================================

@main.group()
def config():
    """Configure Saini settings."""
    pass


@config.command(name='show')
def config_show():
    """Show current configuration."""
    cfg = Config()
    cfg.show()


@config.command(name='pomodoro')
@click.argument('value', type=click.Choice(['on', 'off']))
def config_pomodoro(value):
    """Enable/disable Pomodoro mode."""
    cfg = Config()
    cfg.set_pomodoro(value == 'on')


@config.command(name='idle')
@click.argument('value', type=click.Choice(['on', 'off']))
def config_idle(value):
    """Enable/disable idle detection."""
    cfg = Config()
    cfg.set_idle_detection(value == 'on')


@config.command(name='idle-time')
@click.argument('minutes', type=int)
def config_idle_time(minutes):
    """Set idle threshold in minutes."""
    cfg = Config()
    cfg.set_idle_threshold(minutes)


# ============================================================================
# REPORT COMMANDS
# ============================================================================

@main.group()
def report():
    """Generate time tracking reports."""
    pass


@report.command(name='today')
def report_today():
    """Show today's time tracking."""
    reports = Reports()
    reports.today()


@report.command(name='yesterday')
def report_yesterday():
    """Show yesterday's time tracking."""
    reports = Reports()
    reports.yesterday()


@report.command(name='week')
def report_week():
    """Show this week's time tracking."""
    reports = Reports()
    reports.week()


@report.command(name='project')
@click.argument('project_name', required=False)
def report_project(project_name):
    """Show report for specific project."""
    reports = Reports()
    reports.by_project(project_name)


@main.command()
@click.argument('format', type=click.Choice(['csv', 'json']))
@click.option('--output', '-o', help='Output file name')
def export(format, output):
    """Export tracking data."""
    reports = Reports()
    reports.export(format, output)


# ============================================================================
# PROJECT TREE COMMANDS
# ============================================================================

@main.command()
@click.option('--path', '-p', default='.', help='Root path to generate tree from')
@click.option('--depth', '-d', type=int, help='Maximum depth to traverse')
@click.option('--hidden', '-a', is_flag=True, help='Show hidden files')
@click.option('--no-icons', is_flag=True, help='Disable icons')
@click.option('--size', '-s', is_flag=True, help='Show file sizes')
@click.option('--output', '-o', help='Save tree to file')
@click.option('--format', '-f', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.option('--ignore', '-i', multiple=True, help='Additional patterns to ignore')
@click.option('--analyze', is_flag=True, help='Analyze structure and suggest improvements')
def tree(path, depth, hidden, no_icons, size, output, format, ignore, analyze):
    """Generate project structure tree.
    
    Examples:
        saini tree                          # Show tree of current directory
        saini tree --analyze                # Show tree with structure analysis
        saini tree -p /path/to/project      # Show tree of specific path
        saini tree -d 3                     # Limit depth to 3 levels
        saini tree -d 3 --analyze           # Analyze with depth limit
        saini tree -a                       # Show hidden files
        saini tree -s                       # Show file sizes
        saini tree -a -s --analyze          # Full analysis with sizes
        saini tree -o tree.txt              # Save to file
        saini tree -i "*.pyc" -i "test_*"   # Ignore additional patterns
    """
    project_tree = ProjectTree(
        root_path=path,
        max_depth=depth,
        show_hidden=hidden,
        custom_ignore=set(ignore) if ignore else None,
        show_size=size,
        icons=not no_icons,
        analyze=analyze
    )
    
    if output:
        project_tree.save_to_file(output, format)
    else:
        project_tree.generate()


@main.command(name='tree-ignore')
@click.option('--path', '-p', default='.', help='Root path')
def tree_ignore(path):
    """Generate tree respecting .gitignore patterns."""
    console.print("🚧 Feature coming soon: Tree with .gitignore support", style="yellow")
    # TODO: Implement gitignore-aware tree

# ============================================================================
# MODEL CONVERSION COMMANDS
# ============================================================================
@main.group()
def convert():
    """Convert models between formats (PyTorch/TF → ONNX → CoreML)."""
    pass

@convert.command(name='pytorch-onnx')
@click.argument('model_path')
@click.argument('output_path')
@click.option('--input-shape', '-s', required=True, help='Input shape (e.g., 1,3,224,224)')
@click.option('--input-names', help='Comma-separated input names')
@click.option('--output-names', help='Comma-separated output names')
@click.option('--opset', type=int, default=11, help='ONNX opset version')
@click.option('--no-optimize', is_flag=True, help='Skip optimization')
def convert_pytorch_onnx(model_path, output_path, input_shape, input_names, output_names, opset, no_optimize):
    """Convert PyTorch model to ONNX.
    
    Examples:
        saini convert pytorch-onnx model.pth model.onnx -s 1,3,224,224
        saini convert pytorch-onnx model.pt output.onnx -s 1,3,224,224 --opset 13
    """
    converter = ModelConverter()
    
    kwargs = {
        'input_shape': input_shape,
        'opset_version': opset,
        'optimize': not no_optimize
    }
    
    if input_names:
        kwargs['input_names'] = input_names.split(',')
    if output_names:
        kwargs['output_names'] = output_names.split(',')
    
    success = converter.pytorch_to_onnx(model_path, output_path, **kwargs)
    
    if not success:
        raise click.Abort()

@convert.command(name='tf-onnx')
@click.argument('model_path')
@click.argument('output_path')
@click.option('--opset', type=int, default=11, help='ONNX opset version')
@click.option('--no-optimize', is_flag=True, help='Skip optimization')
def convert_tf_onnx(model_path, output_path, opset, no_optimize):
    """Convert TensorFlow/Keras model to ONNX.
    
    Examples:
        saini convert tf-onnx model.h5 model.onnx
        saini convert tf-onnx saved_model/ model.onnx --opset 13
    """
    converter = ModelConverter()
    
    success = converter.tensorflow_to_onnx(
        model_path,
        output_path,
        opset_version=opset,
        optimize=not no_optimize
    )
    
    if not success:
        raise click.Abort()

@convert.command(name='onnx-coreml')
@click.argument('onnx_path')
@click.argument('output_path')
@click.option('--name', default='ConvertedModel', help='Model name')
@click.option('--target', default='iOS13', 
              type=click.Choice(['iOS13', 'iOS14', 'iOS15', 'iOS16', 'macOS10_15', 'macOS11', 'macOS12']),
              help='Minimum deployment target')
@click.option('--precision', default='FLOAT32',
              type=click.Choice(['FLOAT32', 'FLOAT16']),
              help='Compute precision')
def convert_onnx_coreml(onnx_path, output_path, name, target, precision):
    """Convert ONNX model to CoreML.
    
    Examples:
        saini convert onnx-coreml model.onnx model.mlmodel
        saini convert onnx-coreml model.onnx output.mlmodel --target iOS15 --precision FLOAT16
    """
    converter = ModelConverter()
    
    success = converter.onnx_to_coreml(
        onnx_path,
        output_path,
        model_name=name,
        minimum_deployment_target=target,
        compute_precision=precision
    )
    
    if not success:
        raise click.Abort()

@convert.command(name='auto')
@click.argument('model_path')
@click.argument('output_path')
@click.option('--from', 'source_framework', required=True,
              type=click.Choice(['pytorch', 'tensorflow', 'keras', 'onnx']),
              help='Source framework')
@click.option('--to', 'target_format', required=True,
              type=click.Choice(['onnx', 'coreml']),
              help='Target format')
@click.option('--input-shape', '-s', help='Input shape for PyTorch (e.g., 1,3,224,224)')
@click.option('--name', default='ConvertedModel', help='Model name for CoreML')
@click.option('--target', default='iOS13', help='Deployment target for CoreML')
@click.option('--precision', default='FLOAT32', help='Compute precision for CoreML')
@click.option('--opset', type=int, default=11, help='ONNX opset version')
def convert_auto(model_path, output_path, source_framework, target_format, input_shape, 
                 name, target, precision, opset):
    """Auto-convert between any supported formats.
    
    Examples:
        # PyTorch → ONNX
        saini convert auto model.pth model.onnx --from pytorch --to onnx -s 1,3,224,224
        
        # PyTorch → CoreML (via ONNX)
        saini convert auto model.pt model.mlmodel --from pytorch --to coreml -s 1,3,224,224
        
        # TensorFlow → ONNX
        saini convert auto model.h5 model.onnx --from tensorflow --to onnx
        
        # ONNX → CoreML
        saini convert auto model.onnx model.mlmodel --from onnx --to coreml --target iOS15
    """
    converter = ModelConverter()
    
    kwargs = {
        'model_name': name,
        'deployment_target': target,
        'precision': precision,
        'opset_version': opset,
        'optimize': True
    }
    
    if input_shape:
        kwargs['input_shape'] = input_shape
    
    success = converter.convert(
        model_path,
        output_path,
        source_framework,
        target_format,
        **kwargs
    )
    
    if not success:
        raise click.Abort()

@convert.command(name='batch')
@click.argument('models_dir')
@click.argument('output_dir')
@click.option('--from', 'source_framework', required=True,
              type=click.Choice(['pytorch', 'tensorflow', 'onnx']),
              help='Source framework')
@click.option('--to', 'target_format', required=True,
              type=click.Choice(['onnx', 'coreml']),
              help='Target format')
@click.option('--input-shape', '-s', help='Input shape for PyTorch')
@click.option('--target', default='iOS13', help='Deployment target for CoreML')
def convert_batch(models_dir, output_dir, source_framework, target_format, input_shape, target):
    """Batch convert multiple models.
    
    Examples:
        saini convert batch models/ output/ --from pytorch --to onnx -s 1,3,224,224
        saini convert batch onnx_models/ coreml_models/ --from onnx --to coreml
    """
    converter = ModelConverter()
    
    kwargs = {
        'deployment_target': target,
        'optimize': True
    }
    
    if input_shape:
        kwargs['input_shape'] = input_shape
    
    converter.batch_convert(
        models_dir,
        output_dir,
        source_framework,
        target_format,
        **kwargs
    )


if __name__ == '__main__':
    main()