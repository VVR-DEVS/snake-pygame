import json

class Option:
    value: None

    def __init__(self, value):
        self.value = value

    def __str__(self):
        """String representation of the Option

        Returns:
            _string_: _representation with all parameters of the Option_
        """
        string = ''
        for key, value in self.__dict__.items():
            string += f'{value}'
        return string

    def __repr__(self):
        return self.__str__()
    
    def repr_json(self):
        return self.__dict__

class Setting:
    """Classe para carregar as configurações do jogo de um arquivo JSON
    """

    SETTINGS_FILE = 'settings.json'

    # Types of Settings
    STRING = 'STR'
    SELECT = 'SLT'
    NUMBER = 'NUM'
    BOOLEAN = 'BOL'

    DEFAULT_VALUE = 'DEFAULT'

    # Title to appear on Screen
    name = None
    # Code to identify the Setting
    code = None
    # Type of Setting
    type_set = None
    # Current value of Setting
    value = None
    # Default value for the Setting
    default = None
    # Options for the Setting (Only for SELECT Setting)
    options = None
    # Maximum value for the Setting (Only for NUMBER Setting)
    max = None
    # Minimum value for the Setting (Only for NUMBER Setting)
    min = None

    def __init__(self, name, code, type_set, value, options, max_v, min_v, default=None):
        self.name = name
        self.code = code
        self.type_set = type_set
        self.value = value
        self.default = value
        self.options = options
        self.max = max_v
        self.min = min_v
    
    def __str__(self, list=False):
        """String representation of the Setting

        Returns:
            _string_: _representation with all parameters of the Setting_
        """
        string = ''
        for key, value in self.__dict__.items():
            string += f'    {key}: {value}\n'
        return string + '\n'
    
    def __repr__(self):
        return '\n' + self.__str__(list=True)
    
    @staticmethod
    def decoder(obj):
        if 'options' in obj:
            return Setting(obj['name'], obj['code'], obj['type_set'], obj['value'], obj['options'], obj['max'], obj['min'], default=obj['default'])
        else:
            return Option(obj['value'])
        

    @staticmethod
    def load_settings():
        """Load Settings from JSON file
        """
        with open(Setting.SETTINGS_FILE) as json_file:
            settings = json.loads(json_file.read(), object_hook=Setting.decoder)
            return settings

    @staticmethod
    def save_settings(settings):
        """Save Settings to JSON file
        """

        class ComplexEncoder(json.JSONEncoder):
            """Class for Encoding Nested Objects
            """
            def default(self, obj):
                if hasattr(obj,'repr_json'):
                    return obj.repr_json()
                else:
                    return json.JSONEncoder.default(self, obj)

        with open(Setting.SETTINGS_FILE, 'w') as outfile:
            json.dump(settings, outfile, indent=4, cls=ComplexEncoder)
                
    
    def repr_json(self):
        return dict(name=self.name, code=self.code, type_set=self.type_set, value=self.value, default=self.default, options=self.options, max=self.max, min=self.min)


if __name__ == '__main__':
    settings = Setting.load_settings()
    print(settings)