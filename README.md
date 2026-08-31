# ⏱ Time Tracker

A single-file time tracker. One HTML file, no build step, no dependencies, no account,
no server. Open it and it works — including offline.

**Live:** https://qmanzoor19.github.io/time-tracker/

![built with nothing but HTML, CSS and JS](https://img.shields.io/badge/stack-one%20html%20file-informational)

---

## What it's for

Two questions, and it is built around only these two:

1. **Am I hitting my targets?** Every category carries a daily hour target. Day, week and
   insight views all show logged-vs-target with the signed gap.
2. **Where does the time leak?** Categories marked as a *leak* get charted by hour of day,
   so you can see whether the loss is clustered (worth a rule) or scattered (not worth
   policing).

## How you log

You **paint** the day. 48 half-hour blocks; pick a category, then click or drag across the
blocks you just lived.

| Key | Action |
|---|---|
| `1`–`8` | pick a category |
| `0` | eraser |
| `←` `→` | previous / next day |
| `⌘Z` / `Ctrl+Z` | undo |

This is deliberately **not** a live start/stop timer and **not** an end-of-day journal.
Timers get abandoned the first time you forget to hit stop, and whole-day recall
reliably hides exactly the time you most want to see. The intended rhythm is three
20-second check-ins — lunch, dinner, bed. If you're more than 90 minutes behind, a banner
appears with a single **Fill 14:30 → now** button, which is most of the daily effort.

## Categories

Eight to start — Sleep, Deep work, Korean study, Admin & chores, Health & food, People,
Leisure, Scroll & drift — and there is no limit on how many you add. Everything about a
category is editable in **Setup**: colour, icon, name, kind, daily target, and its position
in the list.

Order matters beyond looks: it sets the paint-palette order, the legend order, and which
number key selects what (the first nine get `1`–`9`).

Each category has a *kind* that drives the scoring:

| Kind | Target means | Example |
|---|---|---|
| `invest` | a floor — reach it | deep work, study, exercise |
| `upkeep` | a floor — neutral maintenance | admin, chores |
| `rest` | a band — hit it, don't exceed it much | sleep |
| `leak` | a **ceiling** — stay under it | scrolling, drift |

**A note on colours.** The eight built-in hues come from a validated categorical palette,
ordered so every adjacent pair stays distinguishable under colour-blindness simulation.
They show up as suggestions inside the colour picker, and are worth preferring. Beyond
those eight you are on your own: nothing stops you picking two blues you cannot tell apart
in the week heatmap. The icons and the table view are what keep the display readable when
the colours stop pulling their weight.

Text drawn on a category — the labels in the day grid — picks black or white by measured
contrast against the fill, so a colour you invent still gets a legible label.

## What it computes

- **Coverage %** — how much of each logged day is actually accounted for. It exists to stop
  the other numbers lying to you: a blank block is not zero, it's *unknown*, and unknown
  time quietly flatters every total.
- **Longest unbroken focus run** — consecutive `invest` blocks.
- **Switches per day** — category changes, as a fragmentation proxy.
- **Leak concentration** — what share of leaked time falls in the worst few hour-slots.
- Week/insight targets scale to *days actually logged*, so a half-logged week isn't reported
  as a failure against seven days of targets.

## Your data

Everything lives in the browser's `localStorage` under `timeTracker.v1`. It is never sent
anywhere — there is no backend to send it to. Consequences worth knowing:

- **Clearing site data deletes your history.** Hit the 💾 button in the top bar to
  download a JSON backup; the app nags you with a banner once a backup is more than a week
  old, and shows the age of your last one under **Setup → Your data**.
- **Devices don't sync.** Phone and laptop keep separate logs.
- CSV export is also available — one row per contiguous run
  (`date, start, end, category, kind, minutes`).

## Running it

Open `index.html`. That's the whole procedure. No `npm install`, no server.

## Development

There is no build. Edit the one file. To syntax-check the embedded JS without Node:

```sh
JSC=/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc
# extract the <script> body to main.js first, then:
$JSC -e "try { new Function(readFile('main.js')); print('OK') } catch (e) { print(e) }"
```

## Licence

MIT — see [LICENSE](LICENSE).
