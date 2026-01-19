# Volume Profile Rectangle Indicator for TradingView

A PineScript v5 indicator that allows you to define a rectangular area on your chart and calculates the total volume within that area.

## Features

- **Customizable Rectangle**: Define exact coordinates using date/time and price inputs
- **Multiple Volume Calculation Methods**:
  - **Total**: Sum all volume for bars within the date range
  - **Bar in Range**: Only count volume from bars completely within the price range
  - **Weighted**: Weight volume by the percentage of each bar that falls within the price range
- **Visual Feedback**: Rectangle is drawn on chart with volume label
- **Real-time Updates**: Volume calculation updates as new bars form
- **Formatted Display**: Volume shown with K/M/B suffixes for readability

## How to Use

### 1. Add to TradingView

1. Open TradingView and go to the Pine Editor (bottom of screen)
2. Create a new indicator
3. Copy the entire contents of `volume_profile_rectangle.pine`
4. Click "Save" and then "Add to Chart"

### 2. Configure the Rectangle

Once added to your chart, click the indicator settings (gear icon) to configure:

#### Rectangle Coordinates
- **Start Date/Time**: Beginning of the time range
- **End Date/Time**: End of the time range
- **Top Price**: Upper boundary of the price range
- **Bottom Price**: Lower boundary of the price range

#### Calculation Settings
- **Volume Method**: Choose how volume is calculated
  - `Total`: Sums all volume for bars in the date range (most inclusive)
  - `Bar in Range`: Only includes bars where both high and low are within price range (most restrictive)
  - `Weighted`: Weights each bar's volume by what percentage of it falls within the price range (most accurate)
- **Max Lookback Bars**: Maximum number of bars to look back for calculation (default: 500, max: 5000)
  - Increase this if your date range extends far into the past
  - Higher values may slow down the indicator but provide more complete data

#### Visual Settings
- **Rectangle Color**: Background color of the rectangle
- **Rectangle Border**: Border color of the rectangle
- **Label Text Color**: Color of the volume text
- **Label Background**: Background color of the label

### 3. Reading the Results

The indicator will:
1. Draw a rectangle on your chart at the specified coordinates
2. Display a label at the top-right corner showing:
   - Formatted volume (e.g., "123.45M")
   - Exact volume in parentheses

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

- **Lookback Limit**: The indicator only looks back a maximum number of bars (default 500, adjustable to 5000)
  - If your date range is older than the lookback limit, some data may be excluded
  - Increase "Max Lookback Bars" in settings if you need to analyze older data
  - Higher lookback values may impact performance
- The indicator recalculates on each bar, which may cause slight delays on lower-powered devices
- Maximum of 500 boxes and labels (PineScript limitation)
- Data availability depends on your TradingView plan and the chart's loaded history

## Tips

- Use the **Weighted** method for most accurate volume profile calculations
- Start with a smaller date range and expand as needed
- If your rectangle doesn't show the expected volume, try increasing "Max Lookback Bars"
- The indicator works on all timeframes, but calculation time increases with more bars
- You can add multiple instances of the indicator to compare different areas
- For recent data (within last 500 bars), the default settings work perfectly

## Technical Notes

- Written in PineScript v5
- Uses `box.new()` for rectangle visualization
- Implements efficient looping for volume calculation
- Provides real-time updates as new bars form

## Support

For issues or questions about this indicator, please refer to the TradingView PineScript documentation or community forums.
