# Volume Profile Rectangle Indicator for TradingView

A PineScript v5 indicator that allows you to define a rectangular area on your chart and calculates the total volume within that area.

## Features

- **Two Coordinate Modes**:
  - **Bars Back Mode** (Recommended): Uses relative bar counts - always works with current chart data
  - **Date/Time Mode**: Uses absolute dates for historical analysis
- **Auto Price Range**: Automatically calculates price range based on chart data (can be manually overridden)
- **Price Level Extensions**: Optional dashed lines extending left and right at top/bottom prices (perfect for support/resistance levels)
- **Volume Delta Analysis**: Calculate buying vs selling pressure with color-coded labels (green for bullish, red for bearish)
- **Multiple Volume Calculation Methods**:
  - **Total**: Sum all volume for bars within the date range
  - **Bar in Range**: Only count volume from bars completely within the price range
  - **Weighted**: Weight volume by the percentage of each bar that falls within the price range
- **Visual Feedback**: Rectangle is drawn on chart with volume label
- **Real-time Updates**: Volume calculation updates as new bars form
- **Formatted Display**: Volume shown with K/M/B suffixes for readability
- **Built-in Debug Plot**: Volume plot visible in data window to verify calculations

## How to Use

### 1. Add to TradingView

1. Open TradingView and go to the Pine Editor (bottom of screen)
2. Create a new indicator
3. Copy the entire contents of `volume_profile_rectangle.pine`
4. Click "Save" and then "Add to Chart"

### 2. Configure the Rectangle

Once added to your chart, click the indicator settings (gear icon) to configure:

#### Rectangle Coordinates

**Mode Selection:**
- **Use Bars Back (Recommended)**: When enabled, uses relative bar counts from current bar (default: ON)
  - **Bars Back to Start**: How many bars back to start the rectangle (default: 100)
  - **Bars Back to End**: How many bars back to end the rectangle (default: 0 = current bar)

- **Date/Time Mode**: When "Use Bars Back" is disabled, uses absolute dates
  - **Start Date/Time**: Beginning of the time range
  - **End Date/Time**: End of the time range

**Price Range:**
- **Auto-Calculate Price Range**: Automatically sets top/bottom prices based on highs/lows in the date range (default: ON)
- **Manual Top Price**: Used when auto-calculate is OFF
- **Manual Bottom Price**: Used when auto-calculate is OFF

#### Calculation Settings
- **Volume Method**: Choose how volume is calculated
  - `Total`: Sums all volume for bars in the date range (most inclusive)
  - `Bar in Range`: Only includes bars where both high and low are within price range (most restrictive)
  - `Weighted`: Weights each bar's volume by what percentage of it falls within the price range (most accurate)

#### Volume Delta
- **Show Volume Delta**: Enable/disable delta calculation (default: ON)
  - When enabled, label shows buying volume minus selling volume
  - Label background turns green for positive delta (more buying), red for negative delta (more selling)
- **Delta Method**: Choose how to classify buying vs selling volume
  - `Close vs Open`: Simple method - if close > open, it's buying volume; else selling (default)
  - `Price Change Weighted`: Weights volume by the percentage price change (close-open)/open

#### Visual Settings
- **Rectangle Color**: Background color of the rectangle
- **Rectangle Border**: Border color of the rectangle
- **Label Text Color**: Color of the volume text
- **Label Background**: Background color of the label

#### Price Level Extensions
- **Show Price Level Extensions**: Enable/disable dashed lines extending from top and bottom prices (default: ON)
- **Line Style**: Choose between Solid, Dashed, or Dotted lines (default: Dashed)
- **Line Color**: Color of the extension lines (default: blue)
- **Line Width**: Thickness of the lines 1-4 (default: 1)

### 3. Reading the Results

The indicator will:
1. Draw a rectangle on your chart covering the specified time and price range
2. Display a label at the top-right corner showing:
   - Formatted volume (e.g., "Vol: 123.45M")
   - Volume delta if enabled (e.g., "Δ +45.2M" for buying pressure or "Δ -23.1M" for selling pressure)
   - Label background color: green for positive delta (bullish), red for negative delta (bearish)
3. Draw dashed lines extending left and right at the top and bottom prices (if enabled)
4. Show volume in the data window (hover over chart to see)

**Default Behavior (No configuration needed):**
- Rectangle covers last 100 bars
- Price range auto-calculated from highs/lows
- Uses "Total" volume method
- Volume delta enabled with color-coded labels
- Dashed extension lines at top/bottom prices
- Should work immediately on any chart

## Volume Calculation Methods Explained

### Total Volume
Includes ALL volume from any bar that falls within the date range, regardless of price.

**Best for**: Getting total trading activity during a time period

### Volume Delta Explained

Volume Delta = Buying Volume - Selling Volume

The indicator approximates buying and selling volume using two methods:

#### Close vs Open (Simple Method)
- If `close > open`: The bar is bullish → entire volume counted as buying
- If `close < open`: The bar is bearish → entire volume counted as selling
- If `close == open`: Neutral → contributes zero to delta

**Best for**: Quick assessment of overall buying/selling pressure

#### Price Change Weighted (Advanced Method)
- Weights volume by the percentage price change: `(close - open) / open`
- A bar that closes 2% higher contributes more than one that closes 0.5% higher
- Captures the intensity of buying/selling pressure

**Best for**: More nuanced analysis where magnitude of price movement matters

#### Interpreting Delta
- **Positive Delta (Green label)**: More buying than selling → Bullish sentiment in that zone
- **Negative Delta (Red label)**: More selling than buying → Bearish sentiment in that zone
- **Near-zero Delta**: Balanced buying and selling → Consolidation/equilibrium

**Use Cases:**
- Identify accumulation zones (positive delta at support)
- Identify distribution zones (negative delta at resistance)
- Confirm breakouts with strong buying/selling pressure
- Spot divergences (price up but negative delta = weak rally)

### Bar in Range
Only includes volume from bars where the **entire bar** (high to low) is within the price range.

**Best for**: Strict volume profile within a specific price level

### Weighted Volume (Recommended)
Calculates what percentage of each bar overlaps with the price range, then multiplies the volume by that percentage.

**Example**: If a bar ranges from $95 to $105, and your rectangle is $90 to $100:
- Overlap is $95 to $100 = $5
- Bar range is $95 to $105 = $10
- Weight = 50%
- Counted volume = 50% of the bar's volume

**Best for**: Most accurate volume profile calculation

## Example Use Cases

### Analyzing Support/Resistance Zones
1. Identify a support or resistance level on your chart
2. Set the price range to cover the zone (e.g., $99.50 to $100.50)
3. Set the date range to cover the period you're interested in
4. Use "Weighted" method to see actual volume traded in that zone
5. Extension lines will project the levels across your entire chart for easy reference

### Comparing Volume Across Time Periods
1. Create multiple instances of the indicator
2. Set the same price range for all
3. Set different date ranges for each
4. Compare volume across different time periods

### Volume Profile Analysis
1. Identify a consolidation area
2. Set the rectangle to cover the entire consolidation
3. Use "Weighted" method for accurate distribution
4. Analyze where volume concentrated within the range

## Limitations

- **Lookback Limit**: When using "Bars Back" mode, limited to specified number of bars
  - Bars Back mode can look back up to 5000 bars
  - Date/Time mode can look back up to 5000 bars from current bar
- The indicator recalculates on each bar update
- Maximum of 500 boxes and labels (PineScript limitation)
- Data availability depends on your TradingView plan and the chart's loaded history
- Auto price calculation only works in "Bars Back" mode

## Tips

- **For most users**: Leave default settings (Bars Back mode, Auto Price, Total volume, Delta enabled) - it just works!
- Use the **Weighted** method for most accurate volume profile calculations
- **Bars Back mode** is more reliable than Date/Time mode for quick analysis
- **Extension lines** are great for marking support/resistance levels that persist across time
- **Volume Delta color coding** provides instant visual feedback on buying/selling pressure
- Look for **positive delta at support levels** to confirm accumulation zones
- Look for **negative delta at resistance levels** to confirm distribution zones
- Check the data window (hover over chart) to verify volume is being calculated
- The indicator works on all timeframes
- You can add multiple instances of the indicator to compare different areas
- For precise price levels, disable "Auto-Calculate Price Range" and set manual prices
- For historical analysis, switch to Date/Time mode and set specific dates
- Disable extension lines if you find them distracting or want a cleaner chart
- Disable delta if you only want total volume without buy/sell breakdown

## Technical Notes

- Written in PineScript v5
- Uses `box.new()` for rectangle visualization with `xloc.bar_time` positioning
- Uses `line.new()` with `extend.both` for price level extensions
- Implements efficient looping with configurable lookback
- Updates rectangle, label, and lines only on last bar for performance
- Volume delta calculated using open/close comparison or price-weighted method
- Label background color dynamically changes based on delta (green/red/neutral)
- Includes volume plot for debugging (visible in data window)
- Default settings designed to work immediately without configuration
- Supports customizable line styles (solid, dashed, dotted)
- Delta calculation respects the selected volume method (Total/Bar in Range/Weighted)

## Support

For issues or questions about this indicator, please refer to the TradingView PineScript documentation or community forums.
