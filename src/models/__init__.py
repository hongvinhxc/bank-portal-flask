from bson.objectid import ObjectId

class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def save(self):
        if not self._id:
            self.collection.insert(self)
            self._id = str(self._id)
        else:
            self._id = ObjectId(self._id)
            self.collection.update(
                { "_id": self._id }, self)
            self._id = str(self._id)

    def reload(self):
        if self._id:
            self.update(self.collection\
                    .find_one({"_id": ObjectId(self._id)}))
            self._id = str(self._id)

    def remove(self):
        if self._id:
            self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()
