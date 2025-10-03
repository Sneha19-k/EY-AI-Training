use university
switched to db university
db.teacher.insertOne({$all.insertOne({
  student_id:1,
  name: "Rahul",
  age:21,
  city:"Mumbai",
  course:"AI",
  marks:85
  })
SyntaxError: Unexpected token, expected "," (1:26)

[0m[31m[1m>[22m[39m[90m 1 |[39m db[33m.[39mteacher[33m.[39minsertOne({$all[33m.[39minsertOne({
 [90m   |[39m                           [31m[1m^[22m[39m
 [90m 2 |[39m   student_id[33m:[39m[35m1[39m[33m,[39m
 [90m 3 |[39m   name[33m:[39m [32m"Rahul"[39m[33m,[39m
 [90m 4 |[39m   age[33m:[39m[35m21[39m[33m,[39m[0m
db.teachers.insertOne({
  student_id:1,
  name: "Rahul",
  age:21,
  city:"Mumbai",
  course:"AI",
  marks:85
  })
{
  acknowledged: true,
  insertedId: ObjectId('68dfbea3fd55df2d9637d3f7')
}
db.teachers.deleteMany()
MongoshInvalidInputError: [COMMON-10001] Missing required argument at position 0 (Collection.deleteMany)
db.teachers.deleteOne({name : "Rahul"})
{
  acknowledged: true,
  deletedCount: 1
}
db.teachers.insertMany([
  { teachers_id: 2, name: "Priya", age: 22, city: "Delhi", subject: "ML"},
  { teachers_id: 3, name: "Arjun", age: 20, city: "Bengaluru", subject: "Data Science" },
  { teachers_id: 4, name: "Neha", age: 23, city: "Hyderabad", subject: "AI" },
  { teachers_id: 5, name: "Vikram", age: 21, city: "Chennai", subject: "ML"}
])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId('68dfc077fd55df2d9637d3f8'),
    '1': ObjectId('68dfc077fd55df2d9637d3f9'),
    '2': ObjectId('68dfc077fd55df2d9637d3fa'),
    '3': ObjectId('68dfc077fd55df2d9637d3fb')
  }
}
db.teachers.find()
{
  _id: ObjectId('68dfc077fd55df2d9637d3f8'),
  teachers_id: 2,
  name: 'Priya',
  age: 22,
  city: 'Delhi',
  subject: 'ML'
}
{
  _id: ObjectId('68dfc077fd55df2d9637d3f9'),
  teachers_id: 3,
  name: 'Arjun',
  age: 20,
  city: 'Bengaluru',
  subject: 'Data Science'
}
{
  _id: ObjectId('68dfc077fd55df2d9637d3fa'),
  teachers_id: 4,
  name: 'Neha',
  age: 23,
  city: 'Hyderabad',
  subject: 'AI'
}
{
  _id: ObjectId('68dfc077fd55df2d9637d3fb'),
  teachers_id: 5,
  name: 'Vikram',
  age: 21,
  city: 'Chennai',
  subject: 'ML'
}
db.teachers.updateMany({subject: "AI"},{$set: {subject: "AIML"}})
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
db.teachers.deleteOne({name: "Arjun"})
