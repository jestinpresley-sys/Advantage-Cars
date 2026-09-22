# Adding a car

Everything on the site counts from one array in `index.html`.
Add an entry there and the fleet page, the featured card, the hero's
"available now" figure, the fleet size, and the "from" price all update
themselves. There is nothing else to change.

---

## The three steps

**1. Prep the photo**

Run this from the site folder — the one with `index.html` in it:

```
python3 prep-photo.py sonata.jpg
```

It crops, resizes and saves straight to `photos/sonata.jpg`. Open that
file and check the framing.

If the roof is cut off, run it again with a higher `--top`:

```
python3 prep-photo.py sonata.jpg --top 35
```

Lower the number if there's too much sky. Default is 25.

**2. Paste the entry**

Open `index.html`, find the block marked
`THE ONLY BLOCK YOU EDIT`, and paste a new entry inside the brackets:

```js
{
  y: 2018,
  name: "Hyundai Sonata",
  trim: "SE",
  cat: "Sedan",
  price: 62,
  ok: true,
  photo: "photos/sonata.jpg",
  specs: ["5 seats","Automatic","4 doors","Bluetooth","Backup camera"]
},
```

Every entry except the last one ends with a comma.

**3. Save and refresh.**

---

## Field reference

| Field | Notes |
|---|---|
| `y` | Model year, a number |
| `name` | Make and model, no year — "Hyundai Sonata" |
| `trim` | Optional. Omit the line entirely if there isn't one |
| `cat` | `"Economy"` or `"Sedan"`. Must match a value in `CATS` |
| `price` | Dollars per day, a number — `62` not `"$62"` |
| `ok` | `true` = bookable. `false` = dimmed with "Notify me" |
| `photo` | Path into `photos/`. The file must exist or the card shows blank |
| `specs` | 4–6 short items. Keep them consistent across cars |

**Taking a car out of service:** set `ok: false`. Don't delete the entry —
deleting it breaks the link and loses the demand signal from people who
tapped "Notify me."

**Adding a new category:** add it to `CATS` as well, or nothing will
filter into it. Filters stay hidden until more than one category is in
stock, so this only matters once the fleet is mixed.

---

## What to collect from the client per car

Send them this list. Everything here is needed before the car can go up.

- Year, make, model, trim
- Daily rate
- Transmission, seats, doors
- Any features worth listing — Bluetooth, backup camera, CarPlay, sunroof
- One photo, three-quarter front angle, whole car in frame, daylight
- Whether it's bookable now or out of service

**Photo guidance worth passing on:** stand at the front corner so you see
the front and one side, get the whole car in frame including the roof and
the bottom of the tires, and shoot in daylight. Avoid shooting into the
sun. One good photo beats five bad ones — the script only uses one.

---

## Folder layout

```
site/
  index.html          the site — the only file you edit
  prep-photo.py       photo prep tool
  photos/             vehicle photos, one per car
    cruze-2014-1lt.jpg
  media/              hero video + its poster frame
    hero.mp4
    hero-poster.jpg
```

Keep the folders together. The paths in `index.html` are relative, so
moving `index.html` on its own breaks every image.

**Viewing it locally:** because the page now loads real files, opening
`index.html` by double-clicking may block them in some browsers. Run a
local server from the site folder instead:

```
python3 -m http.server 8000
```

Then open `http://localhost:8000`. On a real web host it just works.

---

## When to stop doing it this way

This approach is right for a handful of cars. Around **8–10 vehicles**,
move the fleet to a Google Sheet or Airtable that the site reads from.
The client edits a row, the car appears, and nobody has to touch code.
That's a small job when it comes, and it isn't worth doing early.

Bookings are a different question entirely — that's real state that
changes daily and will need a proper system regardless of how the fleet
data is stored.
