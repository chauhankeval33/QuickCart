// Q2 Average events per session ($size, no $unwind needed)
db.sessions.aggregate([
  { $group: {
      _id: null,
      sessions: { $sum: 1 },
      total_events: { $sum: { $size: "$events" } },
      avg_events_per_session: { $avg: { $size: "$events" } }
  } },
  { $project: { _id: 0, sessions: 1, total_events: 1,
                avg_events_per_session: { $round: ["$avg_events_per_session", 2] } } }
]);
