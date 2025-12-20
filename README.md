# Volume Dots (Bookmap Style) - PineScript Indicator

A TradingView PineScript indicator that replicates the volume dots visualization from the Bookmap platform.

## Features

### 📊 Volume Dots Visualization
- **Price Level Analysis**: Divides each bar into multiple price levels and estimates volume at each level
- **Buy/Sell Volume Split**: Separates volume into buy and sell components based on price action
- **Scaled Dots**: Dot size scales with volume magnitude
- **Color-Coded**: Green dots for buy volume, red dots for sell volume

### 📈 Volume Profile (Optional)
- Toggle to show horizontal volume profile bars
- Shows volume distribution across price levels
- Adjustable width and scaling

### 📋 Information Dashboard
- Real-time display of:
  - Buy Volume
  - Sell Volume
  - Volume Delta (Buy - Sell)
  - Total Volume
  - Price Range
  - Market Pressure (Bullish/Bearish)

### 🔔 Alerts
- High Volume Detection (configurable threshold)
- Strong Buy Delta Alert
- Strong Sell Delta Alert

## Installation

1. Open TradingView
2. Click on "Pine Editor" at the bottom of the screen
3. Copy the entire contents of `volume_dots_bookmap.pine`
4. Paste into the Pine Editor
5. Click "Add to Chart"

## Settings

### Volume Dots
- **Dot Size** (1-10): Base size of the volume dots
- **Volume Scale** (0.1-5.0): Scaling factor for dot sizes
- **Show Buy Volume**: Toggle buy volume dots
- **Show Sell Volume**: Toggle sell volume dots

### Colors
- **Buy Volume Color**: Color for buy-side volume (default: green)
- **Sell Volume Color**: Color for sell-side volume (default: red)
- **Neutral Volume Color**: Color for neutral volume (default: gray)

### Display
- **Bars to Display** (10-500): Number of recent bars to show dots for
- **Price Levels per Bar** (5-50): Resolution of price level analysis
- **Min Volume % to Show** (0.01-0.5): Threshold for displaying dots (filters noise)

### Volume Profile
- **Show Volume Profile**: Toggle horizontal volume bars
- **Profile Width**: Width of profile bars in number of candles

### Alerts
- **High Volume Alert**: Threshold as multiple of average volume (e.g., 2.0 = 2x average)

## How It Works

### Volume Calculation
The indicator estimates buy and sell volume by analyzing:
1. **Price Action**: Where the close is relative to high/low
2. **Buy Ratio**: `(close - low) / (high - low)`
3. **Sell Ratio**: `(high - close) / (high - low)`
4. **Volume Split**: Distributes total volume based on these ratios

### Price Level Analysis
For each bar:
1. Divides the price range into configurable levels (default: 10)
2. Estimates volume at each price level
3. Determines if it's buy or sell volume based on position relative to close
4. Plots dots sized by volume magnitude

### Dot Sizing
- Dots are sized using square root scaling for better visualization
- Minimum threshold filters out noise
- Dynamically adapts to recent volume levels

## Comparison to Bookmap

| Feature | Bookmap | This Indicator |
|---------|---------|----------------|
| Volume Dots | ✓ | ✓ |
| Price Level Analysis | ✓ | ✓ (estimated) |
| Buy/Sell Split | ✓ | ✓ (estimated) |
| Real-time Order Flow | ✓ | ✗ (not available in PineScript) |
| Historical Heatmap | ✓ | ✓ (via volume profile) |
| DOM Data | ✓ | ✗ (not available in TradingView) |

**Note**: TradingView does not provide real-time order book data or DOM (Depth of Market) information. This indicator estimates buy/sell volume based on price action, which is a common approximation method.

## Tips for Best Results

1. **Adjust Price Resolution**:
   - Use higher values (20-30) for detailed analysis
   - Use lower values (5-10) for cleaner charts and better performance

2. **Volume Threshold**:
   - Increase to reduce noise on high-volume instruments
   - Decrease to see more detail on low-volume instruments

3. **Timeframes**:
   - Works best on intraday timeframes (1min - 1hour)
   - Higher timeframes will show broader volume patterns

4. **Performance**:
   - Reduce "Bars to Display" if chart becomes slow
   - Lower "Price Levels per Bar" for better performance

5. **Combine with Other Indicators**:
   - Use with traditional volume bars for confirmation
   - Combine with VWAP or volume-weighted indicators
   - Watch for volume dots at key support/resistance levels

## Use Cases

### 1. **Identifying Absorption**
Look for large volume dots at specific price levels where price reverses - indicates absorption of buying/selling pressure.

### 2. **Confirming Breakouts**
Strong breakouts should show increasing buy volume dots above resistance or sell volume dots below support.

### 3. **Divergence Detection**
Price making new highs/lows with decreasing volume dots may indicate weakening momentum.

### 4. **Support/Resistance Validation**
Price levels with historical high volume dots often act as future support/resistance.

### 5. **Delta Analysis**
Watch the volume delta histogram and dashboard for shifts in buying/selling pressure.

## Limitations

- **Estimated Buy/Sell Split**: Cannot access real order flow data; uses price-action based estimates
- **Performance**: Rendering many dots can impact chart performance; adjust settings accordingly
- **Label Limits**: TradingView limits maximum labels per chart (~500); exceeding this will remove oldest labels
- **No Tick Data**: Works with OHLCV bar data, not tick-by-tick data like Bookmap

## Troubleshooting

**Issue**: Dots not appearing
- Check "Bars to Display" setting
- Ensure "Min Volume % to Show" isn't too high
- Verify both buy/sell volume toggles aren't disabled

**Issue**: Chart is slow
- Reduce "Bars to Display" to 50-100
- Lower "Price Levels per Bar" to 5-10
- Disable "Show Volume Profile" if enabled

**Issue**: Dots too small/large
- Adjust "Dot Size" (1-10)
- Modify "Volume Scale" (0.1-5.0)
- Change "Min Volume % to Show" threshold

## Version History

- **v1.0**: Initial release with volume dots, profile, and delta analysis

## License

This indicator is provided as-is for educational and trading purposes.

## Credits

Inspired by the Bookmap platform's innovative volume visualization approach.

---

**Disclaimer**: This indicator provides estimated volume analysis based on price action. For professional order flow analysis with real-time market depth data, consider using dedicated platforms like Bookmap. Past performance is not indicative of future results.
