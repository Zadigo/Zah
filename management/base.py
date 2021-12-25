from argparse import ArgumentParser


class BaseCommand:
    help = ''
    requires_checks = False
    
    def create_parser(self, **kwargs):
        parser = ArgumentParser(description=self.help, **kwargs)
        parser.add_argument('command', type=str, help='Command to execute')
        self.add_arguments(parser)
        return parser
    
    def add_arguments(self, parser: ArgumentParser):
        pass
        
    def execute(self, namespace=None):
        pass


class ProjectCommand(BaseCommand):
    requires_checks = True
