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
            self.collection.update({"_id": self._id}, self)
            self._id = str(self._id)

    def reload(self):
        if self._id:
            self.update(self.collection.find_one({"_id": ObjectId(self._id)}))
            self._id = str(self._id)

    def remove(self):
        if self._id:
            result = self.collection.remove({"_id": ObjectId(self._id)})
            self.clear()
            if result["n"] == 0:
                raise BaseException("Account is not exist")

    def count(self):
        return self.collection.count_documents({})

    def getList(self, pageSize, pageIndex, keyword):
        match = {
            "$or": [
                {"lastname": {"$regex": keyword, "$options": "gi"}},
                {"firstname": {"$regex": keyword, "$options": "gi"}},
                {"address": {"$regex": keyword, "$options": "gi"}},
                {"employer": {"$regex": keyword, "$options": "gi"}},
                {"email": {"$regex": keyword, "$options": "gi"}},
                {"city": {"$regex": keyword, "$options": "gi"}},
                {"gender": {"$regex": keyword, "$options": "gi"}},
                {"age": {"$regex": keyword, "$options": "gi"}},
                {"balance": {"$regex": keyword, "$options": "gi"}},
                {"account_number": {"$regex": keyword, "$options": "gi"}},
            ]
        }
        return self.collection.aggregate(
            [
                {
                    "$facet": {
                        "totalData": [
                            {"$match": match},
                            {
                                "$skip": pageSize * (pageIndex - 1)
                                if pageIndex > 0
                                else 0
                            },
                            {"$limit": pageSize},
                            {"$addFields": {"_id": {"$toString": "$_id"}}},
                        ],
                        "totalCount": [{"$match": match}, {"$count": "count"}],
                    }
                }
            ]
        )
