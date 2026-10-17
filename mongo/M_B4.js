const rows = db.sessions.aggregate([
  {
    $project: {
      version: "$device.app_version",
      pv: { $in: ["product_view", "$events.type"] },
      cart: { $in: ["add_to_cart", "$events.type"] },
      checkout: { $in: ["checkout", "$events.type"] },
      pay: { $in: ["payment_success", "$events.type"] }
    }
  },
  {
    $group: {
      _id: "$version",
      product_view: { $sum: { $cond: ["$pv", 1, 0] } },
      add_to_cart: { $sum: { $cond: ["$cart", 1, 0] } },
      checkout: { $sum: { $cond: ["$checkout", 1, 0] } },
      payment_success: { $sum: { $cond: ["$pay", 1, 0] } }
    }
  },
  {
    $project: {
      product_view: 1,
      add_to_cart: 1,
      checkout: 1,
      payment_success: 1,
      view_to_cart: {
        $multiply: [100, { $divide: ["$add_to_cart", "$product_view"] }]
      },
      cart_to_checkout: {
        $multiply: [100, { $divide: ["$checkout", "$add_to_cart"] }]
      },
      checkout_to_pay: {
        $multiply: [100, { $divide: ["$payment_success", "$checkout"] }]
      }
    }
  },
  { $sort: { _id: 1 } }
]).toArray();

printjson(rows)