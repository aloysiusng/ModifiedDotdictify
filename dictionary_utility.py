def replace_item_in_list(my_list, index, argument):
    if index < 0:
        index = len(my_list) + index
        my_list.pop(index)
        my_list.insert(index, argument)
        return my_list
    else:
        my_list.pop(index)
        my_list.insert(index, argument)
        return my_list

import copy

class dotdictify(dict):
    def __init__(self, value=None):
        self.og_dict = copy.deepcopy(value)     #to prevent the original data from being updated
        self.changes = []
        self.changes.append(self.og_dict)
        if isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        elif value is None:
            pass
        else:
            raise TypeError('expected dict')

    def __setitem__(self, key, value, delimiter = '.'):
        if delimiter in key:
            myKey, restOfKey = key.split(delimiter, 1)
            target = self.setdefault(myKey, dotdictify())
            if not isinstance(target, dotdictify):
                raise KeyError('cannot set "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target)))
            target[restOfKey] = value
        else:
            if isinstance(value, dict) and not isinstance(value, dotdictify):
                value = dotdictify(value)
            dict.__setitem__(self, key, value)

    def __getitem__(self, key, delimiter = '.'):
        if key.isdigit() == True:
            return self[int(key)]
        if delimiter not in key:
            return dict.__getitem__(self, key)
        myKey, restOfKey = key.split(delimiter, 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            raise KeyError('cannot get "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target)))
        return target[restOfKey]

    def final_setter(self, key, value, delimiter = '.'):
        list_of_keys = key.split(delimiter)
        vault = []
        for index, key in enumerate(list_of_keys):
            if key.isdigit() == True:
                key = int(key)      #to get number for 
            if index != len(list_of_keys)-1:
                if vault == []:     #for dict in path
                    vault.append(self.__getitem__(key))
                else:               #for list in path
                    vault.append(vault[index-1].__getitem__(key))
            else:                   #last item in path 
                dict.__setitem__(vault[-1], key, value)
                
    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]


    def last_item_getter(self, key, delimiter='.'):
        list_of_keys = key.split(delimiter)
        vault = []
        for index, key in enumerate(list_of_keys):
            if key.isdigit() == True:
                key = int(key)                    
            if index != len(list_of_keys)-1:
                if vault == []:     #for dict in path
                    vault.append(self.__getitem__(key))
                else:               #for list in path
                    vault.append(vault[index-1].__getitem__(key))
            else:                   #last item in path 
                return vault[-1][key]
                

    def update_dict(self, path, data, delimiter ='.'):
        try:
            if path[-1].isdigit() == True:
                path_list = path.split(delimiter)
                position = path_list.pop()
                path = ""
                for item in path_list:
                    path += item + delimiter
                path = path[:-1]
                to_be_updated = self.last_item_getter(path, delimiter)
                to_be_updated = replace_item_in_list(to_be_updated, int(position), data)
                self.final_setter(path, to_be_updated, delimiter=delimiter)
                self.changes.append(self)
                return self

            else:
                self.final_setter(path, data)
                self.changes.append(self)
                return self
        except Exception as e:
            print(f"The error found was {e}")
            return self.og_dict

    def append_dict(self, path, data, delimiter='.'):
        try:
            path_list = path.split(delimiter)
            position = path_list.pop()
            path = ""
            for item in path_list:
                path += item + delimiter
            path = path[:-1]
            #use self.og_dict to use the original dict
            eop_list = self.last_item_getter(path, delimiter)   #eop = end of path
            eop_list = eop_list[position]
            eop_list.append(data)
            appended_data = {str(position): eop_list }
            self.final_setter(path, appended_data, delimiter=delimiter)
            self.changes.append(self)
            return self
        except:
            raise TypeError("End of path is not a list, you might have selected an item of the list at the end of the path instead")
            return self.og_dict

    def remove_item(self, path, delimiter ='.'):
        index = path[-1]
        try:
            if index.isdigit() != True:
                self.og_dict.final_setter(path, '')
                self.changes.append(self)
                return self
            else:
                path_list = path.split(delimiter)
                position = path_list.pop()
                path = ""
                for item in path_list:
                    path += item + delimiter
                path = path[:-1]      
                to_be_removed = self.last_item_getter(path, delimiter)
                to_be_removed.pop(int(index))
                self.final_setter(path, to_be_removed, delimiter=delimiter)
                self.changes.append(self)
                return self
        except Exception as e:
            print(f"The error found was {e}")
            return self.og_dict

    def __restart__(self):
        self.__init__(self.og_dict)
        return self


##trial
if __name__ == "__main__":
    my_dict2 = {"test":{"alpha":{"start":["9am", "213324"]}}}
    path = 'test.alpha.start.1'
    path2 = 'test.alpha.start'
    data = "10am"
    x = dotdictify(my_dict2)
    test1 = x.update_dict(path, data)
    print(test1)
    data = '11am'
    x.__restart__()
    test2 = x.append_dict(path2, data)
    print(test2)
    x.__restart__()
    test3 = x.remove_item(path)
    print(test3)


