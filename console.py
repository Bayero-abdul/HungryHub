#!/usr/bin/python3
"""this module contains the entry point of the command interpreter.

"""

import cmd
import shlex 
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.restaurant import Restaurant
from models.address import Address
from models.food import Food
from models.order import Order
from models.cart import Cart
from models.cart import CartItem
from models.rating import Rating
from models.payment import Payment
from models.engine.file_storage import FileStorage


classes = {'BaseModel': BaseModel,
                'User': User,
                'Restaurant': Restaurant,
                'Address': Address,
                'Food': Food,
                'Order': Order,
                'Cart': Cart,
                'CartItem': CartItem,
                'Payment': Payment,
                'Rating': Rating
                }


class HungryHubCommand(cmd.Cmd):
    """HungryHub command interpreter"""

    prompt = '(HungryHub) '
    
    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """Creates a new instance of BaseModel, save it and
        print id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save() 

    def do_show(self, line):
        """Prints the string representation of an instance
        based on the class name and id."""

        args = line.split()
        if len(args) < 1:
            self.default("** class name missing **")
        elif args[0] not in classes:
            self.default("** class doesn't exist **")
        elif len(args) < 2:
            self.default("** instance id missing **")
        else:
            cls = args[0]
            Id = args[1]
            instance = cls + "." + Id
            instances = storage.all()
            if instance in instances:
                print(instances[instance])
            else:
                self.default("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""

        args = line.split()
        if len(args) < 1:
            self.default("** class name missing **")
        elif args[0] not in classes:
            self.default("** class doesn't exist **")
        elif len(args) < 2:
            self.default("** instance id missing **")
        else:
            cls = args[0]
            Id = args[1]
            instance = cls + "." + Id
            instances = storage.all()
            if instance in instances:
                del instances[instance]
                storage.save()
            else:
                self.default("** no instance found **")

    def do_all(self, arg):
        """prints the list of all objects stored."""

        if arg and arg not in classes:
            self.default("** class doesn't exist **")
        elif not arg:
            objs = storage.all()
            print([str(v) for v in objs.values()])
        elif arg:
            objs = storage.all()
            print([str(objs[k]) for k in objs if k.split('.')[0] == arg])

    def do_update(self, line):
        """Updates an instance based on the class name and id by
        adding or updating attribute."""

        args = line.split()
        if len(args) < 1:
            self.default("** class name missing **")
        elif args[0] not in classes:
            self.default("** class doesn't exist **")
        elif len(args) < 2:
            self.default("** instance id missing **")
        else:
            cls = args[0]
            Id = args[1]
            inst = cls + "." + Id
            instances = storage.all()
            if inst in instances:
                if len(args) < 3:
                    self.default("** attribute name missing **")
                
                """if dictionary of attrs is passed."""
                try:
                    if type(eval(args[2].replace("|", ' '))) is dict:
                        dict_attrs = eval(args[2].replace("|", ' '))
                        for attr, value in dict_attrs.items():
                            setattr(instances[inst], attr, value)
                        instances[inst].save()
                except NameError:
                    if len(args) < 4:
                        self.default("** value missing **")
                    else:
                        attr = args[2]
                        value = args[3]
                        if attr in instances[inst].__dict__:
                            setattr(instances[inst], attr, value)
                        else:
                            setattr(instances[inst], attr, value)
                        instances[inst].save()
            else:
                self.default("** no instance found **")

    def do_count(self, arg):
        """counts the number of instances a class has."""

        objs = storage.all()
        print(len([objs[k] for k in objs if k.split('.')[0] == arg]))

    def do_EOF(self, arg):
        """EOF(end of file) i.e Ctrl+D"""

        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""

        return True

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed."""

        parsed_tup = cmd.Cmd.parseline(self, line)
        tmp = parsed_tup[-1].split('.')
        if len(tmp) == 2:
            cmd_inst = tmp[1].split('(')
            if len(cmd_inst) < 2:
                return parsed_tup
            command = cmd_inst[0]
            inst = cmd_inst[1]
            cls = tmp[0]
            if len(inst) > 1:
                if command == 'update':
                    arg = inst.split('{')

                    """if dictionary of attrs is passed."""
                    if len(arg) == 2:
                        Id = arg[0][:-2].replace('"', '')
                        attrs = '{' + arg[1][:-1].replace(" ", '|')
                        line = f'{command} {cls} {Id} {attrs}'
                        return cmd.Cmd.parseline(self, line)

                    arg = inst.split(', ')
                    if len(arg) == 1:
                        Id = arg[0].replace('"', '')
                        line = f'{command} {cls} {Id}'
                    elif len(arg) == 2:
                        Id = arg[0].replace('"', '')
                        attr = arg[1].replace('"', '')
                        line = f'{command} {cls} {Id} {attr[:-1]}'
                    else:
                        Id = arg[0].replace('"', '')
                        attr = arg[1].replace('"', '')
                        val = arg[2].replace('"', '')
                        line = f'{command} {cls} {Id} {attr} {val[:-1]}'
                else:
                    line = f'{command} {cls} {inst[1:-2]}'
            else:
                line = f'{command} {cls}'
            parsed_tup = cmd.Cmd.parseline(self, line)
        return parsed_tup

    def emptyline(self):
        """Ignores when empty line or ENTER is being entered"""

        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns."""

        print(line)


if __name__ == '__main__':
    HungryHubCommand().cmdloop()
