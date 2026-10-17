// Find the newest session and calculate the last 7 days
const newest = db.sessions.find().sort({session_start: -1}).limit(1).next().session_start;
const since = new Date(newest.getTime() - 7 * 24 * 60 * 60 * 1000);

// Find a customer with the most sessions in that period
const cid = db.sessions.aggregate([
  {$match: {session_start: {$gte: since}}},
  {$group: {_id: "$customer_id", n: {$sum: 1}}},
  {$sort: {n: -1}}, {$limit: 1}
]).next()._id;

// Query
const q = {customer_id: cid, session_start: {$gte: since}};

// BEFORE index
print("BEFORE:");
printjson(db.sessions.find(q).explain("executionStats").executionStats);

// Create index
db.sessions.createIndex(
  {customer_id: 1, session_start: -1},
  {name: "customer_recent"}
);

// AFTER index
print("AFTER:");
printjson(db.sessions.find(q).explain("executionStats").executionStats);