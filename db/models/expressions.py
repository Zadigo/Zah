

class Expression:
    SELECT = 'SELECT {} FROM {} {}'
    
    @staticmethod
    def parse_expression(expression):
        try:
            tokens = expression.split('__')
        except:
            tokens = expression
        return tokens
    
    def parse_expressions(self, expressions: dict):
        items = []
        for expression, value in expressions.items():
            result = self.parse_expression(expression)
            items.append((result, value))
        return items
