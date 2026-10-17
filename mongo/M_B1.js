// Convert session_start and every event ts to real Date values so date filters and indexes work properly.
db.sessions.updateMany({}, [
  { $set: {
      session_start: { $toDate: "$session_start" },
      events: { $map: { input: "$events", as: "e",
                        in: { $mergeObjects: ["$$e", { ts: { $toDate: "$$e.ts" } }] } } }
  } }
]);
 
// Sanity checks: expect 5982 documents, 5982 distinct session_ids, 1500 distinct customers
print("documents:", db.sessions.countDocuments());
print("distinct session_id:", db.sessions.distinct("session_id").length);
print("distinct customer_id:", db.sessions.distinct("customer_id").length);
printjson(db.sessions.findOne({}, { _id: 0, session_id: 1, session_start: 1 }));

// Q1 Sessions per device.os
db.sessions.aggregate([
  { $group: { _id: "$device.os", sessions: { $sum: 1 } } },
  { $sort: { sessions: -1 } }
]);
