// Q3 Funnel: sessions that reached each stage, plus step-to-step conversion %.
// A session "reached" a stage if any of its events has that type.
db.sessions.aggregate([
  { $project: {
      pv: { $in: ["product_view",    "$events.type"] },
      ac: { $in: ["add_to_cart",     "$events.type"] },
      co: { $in: ["checkout",        "$events.type"] },
      ps: { $in: ["payment_success", "$events.type"] } } },
  { $group: {
      _id: null,
      product_view:    { $sum: { $cond: ["$pv", 1, 0] } },
      add_to_cart:     { $sum: { $cond: ["$ac", 1, 0] } },
      checkout:        { $sum: { $cond: ["$co", 1, 0] } },
      payment_success: { $sum: { $cond: ["$ps", 1, 0] } } } },
  { $project: {
      _id: 0, product_view: 1, add_to_cart: 1, checkout: 1, payment_success: 1,
      view_to_cart_pct:     { $round: [{ $multiply: [100, { $divide: ["$add_to_cart", "$product_view"] }] }, 2] },
      cart_to_checkout_pct: { $round: [{ $multiply: [100, { $divide: ["$checkout", "$add_to_cart"] }] }, 2] },
      checkout_to_pay_pct:  { $round: [{ $multiply: [100, { $divide: ["$payment_success", "$checkout"] }] }, 2] },
      overall_view_to_pay_pct: { $round: [{ $multiply: [100, { $divide: ["$payment_success", "$product_view"] }] }, 2] } } }
]);