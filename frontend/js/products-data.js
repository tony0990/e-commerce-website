/**
 * PremiumStore - Complete Product Data Engine
 * All asset paths encoded correctly. No duplicates. One source of truth.
 */

const PRODUCTS = [
  // ── CHAIRS / FURNITURE ─────────────────────────────────────────────────────
  { id: 1,  cat: "Furniture", folder: "chair", file: "chair.png",                                                         name: "Premium Ergonomic Office Chair",              price: 349.99 },
  { id: 2,  cat: "Furniture", folder: "chair", file: "Comfortable Office Chair with a Soft and Cozy Design.jpg",          name: "Comfort Pro Padded Office Chair",             price: 229.99 },
  { id: 3,  cat: "Furniture", folder: "chair", file: "Elite Black Gaming Chair with Ergonomic Design and Chrome Accents.jpg", name: "Elite Black Gaming Chair",               price: 299.99 },
  { id: 4,  cat: "Furniture", folder: "chair", file: "Dowinx Gaming Chair Ergonomic Racing Style Recliner with Massage Lumbar Support, Office Armchair for Computer PU Leather E-Sports Gamer Chairs with Footrest, Black&Purple.jpg", name: "Dowinx Racing Recliner Gaming Chair",         price: 279.99 },
  { id: 5,  cat: "Furniture", folder: "chair", file: "Office Chair Black,Reclining Gaming Computer Chair Ergonomics Executive Chair with Headrest and Lumbar Support Racing PC Chair with Padded Armrests Swivel Desk Chair_ AmazonSmile_ Kitchen & Home.jpg", name: "Executive Ergonomic Recliner Chair", price: 319.99 },
  { id: 6,  cat: "Furniture", folder: "chair", file: "Office chairs with back support.jpg",                               name: "Lumbar Support Office Chair",                 price: 199.99 },
  { id: 7,  cat: "Furniture", folder: "chair", file: "Gaming & Streaming Chairs - Ergonomic, Reclining & Long-Hour Comfort.jpg", name: "Pro Streamer Ergonomic Chair",        price: 389.99 },
  { id: 8,  cat: "Furniture", folder: "chair", file: "Best Gaming Chairs & Desk Setup.jpg",                               name: "Ultimate Gaming Desk + Chair Bundle",          price: 599.99 },
  { id: 9,  cat: "Furniture", folder: "chair", file: "Setup.jpg",                                                         name: "Minimal Battlestation Desk Setup",             price: 749.99 },
  { id: 10, cat: "Furniture", folder: "chair", file: "download.jpg",                                                      name: "Modern Adjustable Height Desk Chair",         price: 259.99 },
  { id: 11, cat: "Furniture", folder: "chair", file: "download (25).jpg",                                                 name: "Mesh Back Task Chair",                        price: 179.99 },

  // ── ELECTRONICS ────────────────────────────────────────────────────────────
  { id: 12, cat: "Electronics", folder: "electronics", file: "electronics.png",                                           name: "Smart Home Electronics Suite",                price: 1299.99 },
  { id: 13, cat: "Electronics", folder: "electronics", file: "JBL Charge 3 Waterproof Bluetooth Speaker -Black (Renewed).jpg", name: "JBL Charge 3 Waterproof Bluetooth Speaker", price: 129.99 },
  { id: 14, cat: "Electronics", folder: "electronics", file: "Acoustic Energy 300 Series Speakers.jpg",                  name: "Acoustic Energy 300 Series Speakers",         price: 549.00 },
  { id: 15, cat: "Electronics", folder: "electronics", file: "Portable Charger Power Bank 40800mAh with 3 Built-in Cables.jpg", name: "40800mAh Portable Power Bank",          price: 49.99 },
  { id: 16, cat: "Electronics", folder: "electronics", file: "10 Game-Changing Gadget Gifts Your Dad Will___.jpg",        name: "Top Gadget Gift Bundle",                      price: 89.99 },
  { id: 17, cat: "Electronics", folder: "electronics", file: "Solo il Meglio dalle Notizie _ StraNotizie_it.jpg",         name: "Minimalist Smart Display Dock",               price: 79.99 },

  // ── FASHION ────────────────────────────────────────────────────────────────
  { id: 18, cat: "Fashion", folder: "fashion", file: "Louis Vuitton Bag.jpg",                                             name: "Louis Vuitton Luxury Leather Bag",            price: 2450.00 },
  { id: 19, cat: "Fashion", folder: "fashion", file: "Saint Laurent Classic Monogram Leather Tote _ Bragmybag.jpg",      name: "Saint Laurent Monogram Tote Bag",             price: 1890.00 },
  { id: 20, cat: "Fashion", folder: "fashion", file: "Letter Embossed Square Bag.jpg",                                   name: "Letter Embossed Square Shoulder Bag",         price: 89.99 },
  { id: 21, cat: "Fashion", folder: "fashion", file: "black bag.jpg",                                                     name: "Classic Black Leather Crossbody Bag",         price: 65.00 },
  { id: 22, cat: "Fashion", folder: "fashion", file: "ZITY Flannel Plaid Shirt for Men Regular Fit Long Sleeve Casual Button Down Shirts 07-Grey 3XL at Amazon Men's Clothing store.jpg", name: "ZITY Flannel Plaid Long Sleeve Shirt", price: 34.99 },
  { id: 23, cat: "Fashion", folder: "fashion", file: "Round Neck Knitted Pullover Sweater - Dark Gray _ L.jpg",          name: "Round-Neck Knit Pullover Sweater",            price: 49.99 },
  { id: 24, cat: "Fashion", folder: "fashion", file: "Negro elegante.jpg",                                               name: "Elegant Black Formal Blazer",                 price: 129.00 },
  { id: 25, cat: "Fashion", folder: "fashion", file: "Men's Minimalist Pure White Outdoor Casual Flat Sneakers, Lightweight Daily Versatile Lace-Up Skate Shoes, Student Hiking Shoes, Couple Casual White Shoes.jpg", name: "Minimalist White Casual Sneakers", price: 74.99 },
  { id: 26, cat: "Fashion", folder: "fashion", file: "download.jpg",                                                      name: "Casual Streetwear Essential Tee",             price: 29.99 },
  { id: 27, cat: "Fashion", folder: "fashion", file: "download (25).jpg",                                                 name: "Contemporary Urban Hoodie",                   price: 59.99 },
  { id: 28, cat: "Fashion", folder: "fashion", file: "download (26).jpg",                                                 name: "Premium Denim Jacket",                        price: 89.00 },
  { id: 29, cat: "Fashion", folder: "fashion", file: "fashion.png",                                                       name: "Seasonal Collection Lookbook",                price: 49.99 },

  // ── HOME & LIVING ──────────────────────────────────────────────────────────
  { id: 30, cat: "Home & Living", folder: "home", file: "home.png",                                                       name: "Modern Living Room Interior Set",             price: 1499.00 },
  { id: 31, cat: "Home & Living", folder: "home", file: "Coffee Table, Rectangular Glass Coffee Table with Open Storage Shelf and Drawer for Living Room and Office.jpg", name: "Rectangular Glass Coffee Table", price: 279.00 },
  { id: 32, cat: "Home & Living", folder: "home", file: "Greenco 4 Cube Intersecting Shelves, Easy-to-Assemble Floating Wall Mount Shelves for Bedrooms and Living Rooms, Natural Finish.jpg", name: "Greenco 4-Cube Wall Mount Shelves", price: 89.99 },
  { id: 33, cat: "Home & Living", folder: "home", file: "BEVERDY 63_ x 24_ Full Length Mirror with Stand, Full Length Mirror Wall Mounted, Floor Mirror, Irregular Wavy Mirror, Flannel Wrapped Wooden Frame Mirror, Full Body Mirror, Purple.jpg", name: "BEVERDY Full-Length Floor Mirror", price: 159.99 },
  { id: 34, cat: "Home & Living", folder: "home", file: "Genuine Leather Rocking Recliner.jpg",                          name: "Genuine Leather Rocking Recliner",            price: 699.00 },
  { id: 35, cat: "Home & Living", folder: "home", file: "Real Leather Electric Recliner Cinema Chair in Grey _ Power Seat With Massage, Adjustable Headrest & Power Lumbar Support _ Milano _ The Sofa Shop.jpg", name: "Electric Leather Cinema Recliner", price: 1199.00 },
  { id: 36, cat: "Home & Living", folder: "home", file: "10 Great Armchairs For Your Home.jpg",                          name: "Classic Fabric Armchair",                     price: 449.00 },
  { id: 37, cat: "Home & Living", folder: "home", file: "DIY Built In Ikea Pax Wardrobes - Bright Green Door.jpg",       name: "Built-In Wardrobe System (Pax-Style)",        price: 599.00 },
  { id: 38, cat: "Home & Living", folder: "home", file: "download.jpg",                                                   name: "Minimalist Wooden Side Table",                price: 129.00 },
  { id: 39, cat: "Home & Living", folder: "home", file: "download (25).jpg",                                              name: "Scandinavian Bedside Lamp",                   price: 69.99 },
  { id: 40, cat: "Home & Living", folder: "home", file: "download (26).jpg",                                              name: "Boho Woven Wall Hanging Decor",               price: 39.99 },

  // ── WATCHES ───────────────────────────────────────────────────────────────
  { id: 41, cat: "Watches", folder: "watch", file: "watch.png",                                                           name: "Luxury Heritage Chronograph",                 price: 1299.00 },
  { id: 42, cat: "Watches", folder: "watch", file: "Maurice Lacroix Watch Pontos S Mens  PT6008-SS001-331-1 Watch.jpg", name: "Maurice Lacroix Pontos S Men's Watch",       price: 2199.00 },
  { id: 43, cat: "Watches", folder: "watch", file: "Tissot Couturier Men's Watch Chronograph Quartz T0356171605100, Black, Strap_.jpg", name: "Tissot Couturier Quartz Chronograph", price: 649.00 },
  { id: 44, cat: "Watches", folder: "watch", file: "Stainless Steel Business Casual Quartz Wristwatch And 1pc Link Chain Bracelet Set For Men.jpg", name: "Stainless Steel Quartz Wristwatch + Bracelet", price: 189.00 },
  { id: 45, cat: "Watches", folder: "watch", file: "Womens Rolex Datejust Watch 16200 _ 36Mm _ Blue Mother Of Pearl Roman.jpg", name: "Women's Rolex Datejust – Blue MOP Dial", price: 8499.00 },
  { id: 46, cat: "Watches", folder: "watch", file: "Womens Rolex Datejust Watch 16233 _ 36Mm _ Pink Roman Dial _ Jubilee B.jpg", name: "Women's Rolex Datejust – Pink Roman Dial", price: 8999.00 },
  { id: 47, cat: "Watches", folder: "watch", file: "Iced Out Rolex Datejust 36 MM _ Stainless Steel _ 16_5 Carats of Diamo.jpg", name: "Iced-Out Rolex Datejust 36mm Diamond", price: 24999.00 },
  { id: 48, cat: "Watches", folder: "watch", file: "Men's Watches _ Nordstrom.jpg",                                      name: "Men's Premium Watch Collection",              price: 399.00 },
  { id: 49, cat: "Watches", folder: "watch", file: "Ladies And Men's Rolex Watches.jpg",                                 name: "Rolex Signature Couple Set",                  price: 15499.00 },
  { id: 50, cat: "Watches", folder: "watch", file: "As always, simple is best___.jpg",                                   name: "Minimalist Field Watch",                      price: 249.00 },
  { id: 51, cat: "Watches", folder: "watch", file: "download.jpg",                                                       name: "Vintage-Inspired Dress Watch",                price: 179.00 },
  { id: 52, cat: "Watches", folder: "watch", file: "download (25).jpg",                                                  name: "Sport Chrono Diver Watch",                    price: 329.00 },
  { id: 53, cat: "Watches", folder: "watch", file: "viral story.jpg",                                                    name: "Trending Unisex Statement Watch",              price: 219.00 },
];

const DESCRIPTIONS = {
  Furniture: [
    "Designed for long-hours of productivity and comfort, this chair combines premium foam cushioning with an adjustable lumbar system. The breathable mesh back keeps you cool during extended work sessions. With smooth 360° swivel and height adjustment, it adapts perfectly to any desk setup.",
    "This ergonomic masterpiece is built for the modern professional. High-density foam seating, adjustable armrests, and a sturdy aluminum base deliver both luxury and durability. Whether you're gaming, coding, or designing, this chair has your back—literally.",
    "Transform your workspace with a chair that prioritizes your health and comfort. The multi-zone lumbar support system, tilt-tension control, and breathable upholstery provide hours of fatigue-free sitting. A timeless, minimal design that fits any décor."
  ],
  Electronics: [
    "Engineered for audiophiles and tech enthusiasts, this device delivers crystal-clear sound with rich bass response. IPX7 waterproof rating keeps it protected from splashes and brief submersion. Seamlessly connects via Bluetooth 5.0 with 12-hour battery life.",
    "Built with cutting-edge technology to keep you powered and connected. The ultra-high-capacity battery cell supports fast charging for multiple devices simultaneously. Compact and travel-friendly with smart circuit protection.",
    "An essential gadget for the modern home. Features seamless smart-home integration, intuitive touch controls, and a sleek minimalist design. Works with all major voice assistants and can be configured in under 60 seconds."
  ],
  Fashion: [
    "Crafted from full-grain, sustainably sourced leather, this piece is built to age beautifully. Precision stitching and solid brass hardware ensure decades of durability. An iconic design that transcends seasonal trends—this is investment dressing at its finest.",
    "A wardrobe staple redefined for the modern wearer. Premium cotton blend ensures a relaxed yet tailored fit. Thoughtful details like reinforced seams, quality YKK zippers, and fade-resistant dye make this a piece you'll reach for again and again.",
    "Designed for both style and practicality. Multiple interior pockets, a secure magnetic closure, and an adjustable strap make this perfect for daily commutes or weekend adventures. Available in a range of colorways to match every aesthetic."
  ],
  "Home & Living": [
    "Elevate your home with furniture that blends form and function. Crafted from sustainably harvested solid wood with a hand-applied finish that highlights natural grain patterns. Precision-engineered joints ensure stability for generations to come.",
    "A statement piece that anchors any room with quiet sophistication. The designer's touch is evident in every curve and proportion, creating harmony between different furniture styles. Easy assembly with included hardware and clear step-by-step instructions.",
    "Introduce warmth and character to your living space. Each piece is handcrafted with attention to texture and proportion, ensuring unique variations that add authenticity. Tested to withstand daily family use without sacrificing elegance."
  ],
  Watches: [
    "A mastery of Swiss mechanical engineering wrapped in a 40mm stainless steel case. The sapphire crystal caseback reveals the decorated movement within, featuring 25 jewels and a 72-hour power reserve. Water-resistant to 100M for everyday confidence.",
    "Precision quartz movement chronograph with 1/10-second accuracy. Polished and brushed stainless steel case and bracelet. Scratch-resistant sapphire crystal. A professional-grade timepiece at an accessible price point.",
    "Timeless elegance meets modern craftsmanship. The sunburst-finished dial changes depth and character with different lighting conditions, making this watch a conversation piece at any gathering. Scratch-resistant hardened mineral crystal, 50M water resistance."
  ]
};

function buildProducts() {
  return PRODUCTS.map((p, idx) => {
    const descArr = DESCRIPTIONS[p.cat] || DESCRIPTIONS["Furniture"];
    const desc = descArr[idx % descArr.length];
    return {
      id: p.id,
      name: p.name,
      image: `assets/${p.folder}/${encodeURIComponent(p.file)}`,
      category: p.cat,
      price: p.price,
      description: desc,
      rating: (4.1 + Math.random() * 0.9).toFixed(1),
      reviews: Math.floor(120 + Math.random() * 880),
    };
  });
}

const productsData = buildProducts();
export default productsData;
