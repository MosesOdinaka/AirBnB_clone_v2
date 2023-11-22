#!/usr/bin/python3
"""Console for the AirBnB application"""
import cmd
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter entry point
    """
    prompt = "(hbnb) "
    __classes = {"BaseModel", "User", "City", "State", "Amenity", "Place",
                 "Review"}

    def emptyline(self):
        """Handles empty input lines"""
        pass

    def do_quit(self, line):
        """Exits the program upon receiving the quit command"""
        return True

    def do_EOF(self, line):
        """Exits the program at the end of the file"""
        print("")
        return True

    def do_create(self, line):
        """Generates a new instance of BaseModel and saves it"""
        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        class_name, params = args[0], args[1:]

        kwargs = {}
        for param in params:
            key, val = param.split("=")
            val = val.strip('"').replace("_", " ") if val[0] == '"' else eval(val, {}, {})
            kwargs[key] = val

        try:
            obj = eval(class_name)(**kwargs)
        except NameError:
            print("** class doesn't exist **")
            return

        print(obj.id)
        obj.save()

    def do_show(self, line):
        """Displays the string representation of an instance"""
        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        class_name, instance_id = args[0], args[1] if len(args) > 1 else None

        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if not instance_id:
            print("** instance id missing **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

    print(storage.all()[key])

    def do_destroy(self, line):
        """Removes an instance based on the class name and id"""
        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        class_name, instance_id = args[0], args[1] if len(args) > 1 else None

        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if not instance_id:
            print("** instance id missing **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Displays all string representations of all instances
        Exceptions:
            NameError: Raised when the object name does not exist
        """

        if not line:
            obj = storage.all()
            print([obj[key].__str__() for key in obj])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            obj = storage.all(eval(args[0]))
            print([obj[key].__str__() for key in obj])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Modifies an instance by adding or updating an attribute"""
        if not line:
            print("** class name missing **")
            return

        args = line.split(" ")
        class_name, instance_id, attr_name, attr_val = (args + [None] * 4)[:4]

        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if not instance_id:
            print("** instance id missing **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if not attr_name:
            print("** attribute name missing **")
            return

        if not attr_val:
            print("** value missing **")
            return

        instance = storage.all()[key]
        try:
            instance.__dict__[attr_name] = eval(attr_val)
        except Exception:
            instance.__dict__[attr_name] = attr_val

        instance.save()

    def count(self, line):
        """counts the number of instances of a class
        """
        counter = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """Removes spaces from the argument and returns a command string
        Args:
            args: List of input arguments
        Returns:
            Returns a string of arguments
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """Fetches all instances of a class and
        counts the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
