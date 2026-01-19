# Volume Profile Rectangle Indicator for TradingView

A PineScript v5 indicator that allows you to define a rectangular area on your chart and calculates the total volume within that area.

## Features

- **Two Coordinate Modes**:
  - **Bars Back Mode** (Recommended): Uses relative bar counts - always works with current chart data
  - **Date/Time Mode**: Uses absolute dates for historical analysis
- **Auto Price Range**: Automatically calculates price range based on chart data (can be manually overridden)
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

#### Visual Settings
- **Rectangle Color**: Background color of the rectangle
- **Rectangle Border**: Border color of the rectangle
- **Label Text Color**: Color of the volume text
- **Label Background**: Background color of the label

### 3. Reading the Results

The indicator will:
1. Draw a rectangle on your chart covering the specified time and price range
2. Display a label at the top-right corner showing:
   - Formatted volume (e.g., "123.45M")
   - Exact volume below
3. Show volume in the data window (hover over chart to see)

**Default Behavior (No configuration needed):**
- Rectangle covers last 100 bars
- Price range auto-calculated from highs/lows
- Uses "Total" volume method
- Should work immediately on any chart

## Volume Calculation Methods Explained

### Total Volume
Includes ALL volume from any bar that falls within the date range, regardless of price.

**Best for**: Getting total trading activity during a time period

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

- **For most users**: Leave default settings (Bars Back mode, Auto Price, Total volume) - it just works!
- Use the **Weighted** method for most accurate volume profile calculations
- **Bars Back mode** is more reliable than Date/Time mode for quick analysis
- Check the data window (hover over chart) to verify volume is being calculated
- The indicator works on all timeframes
- You can add multiple instances of the indicator to compare different areas
- For precise price levels, disable "Auto-Calculate Price Range" and set manual prices
- For historical analysis, switch to Date/Time mode and set specific dates

## Technical Notes

- Written in PineScript v5
- Uses `box.new()` for rectangle visualization with `xloc.bar_time` positioning
- Implements efficient looping with configurable lookback
- Updates rectangle and label only on last bar for performance
- Includes volume plot for debugging (visible in data window)
- Default settings designed to work immediately without configuration

## Support

For issues or questions about this indicator, please refer to the TradingView PineScript documentation or community forums.
