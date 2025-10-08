# TaskWright Database Query Session

## Database Structure Overview

Three main tables in TaskWrightDb database:

### 1. Items Table
- Product catalog with pricing, inventory, and product details
- Key fields: ID (int), PartNum (nvarchar 50), Brand (varchar 50), StockItem (bit)
- Primary key: ID (identity)

### 2. Tasks Table  
- Orders/quotes with customer info, billing, shipping, and order metadata
- Key fields: ID (int), Company (nvarchar 128), SaleDate (char 15), SO_Status (bit)
- Date stored as string format in SaleDate field
- SO_Status: bit field (0/1) indicating order status

### 3. OrderItems Table
- Line items linking Tasks to Items with quantities and pricing  
- Key fields: TaskID (int), ItemNum (nvarchar 50), Quantity (int)
- ItemNum references Items.PartNum (not Items.ID)

## Query Requirements
Show MTU brand items with total quantities sold since January 1, 2023:
- Filter: Brand = 'MTU' AND StockItem = 0
- Only include tasks where SO_Status = 1
- Date filter: SaleDate >= '2023-01-01'
- Group by item and sum quantities across all qualifying orders

## Final Query

```sql
SELECT 
    'Jan 01, 2023 - Current' as DateRange,
    i.PartNum,
    i.Description,
    i.Brand,
    SUM(oi.Quantity) as TotalQtySold,
    STRING_AGG(CAST(t.ID AS VARCHAR) + ' (Qty: ' + CAST(oi.Quantity AS VARCHAR) + ') (' + ISNULL(t.Company, 'No Company') + ')', ', ') as TaskIDs_Qty_Companies
FROM TaskWrightDb.dbo.Items i
INNER JOIN TaskWrightDb.dbo.OrderItems oi ON i.PartNum = oi.ItemNum
INNER JOIN TaskWrightDb.dbo.Tasks t ON oi.TaskID = t.ID
WHERE 
    i.Brand = 'MTU'
    AND i.StockItem = 0
    AND t.SO_Status = 1
    AND TRY_CONVERT(datetime, t.SaleDate) >= '2023-01-01'
    AND t.SaleDate IS NOT NULL
    AND t.SaleDate <> ''
GROUP BY 
    i.PartNum, i.Description, i.Brand
ORDER BY 
    TotalQtySold DESC
```

## Key Issues Resolved
1. **Type conversion error**: ItemNum is nvarchar, not int - join on PartNum instead of ID
2. **Date handling**: SaleDate stored as char(15) - use TRY_CONVERT for safe conversion
3. **Dynamic output**: STRING_AGG to show TaskID, quantity per task, and company name
4. **Date range**: Fixed to show filter date range rather than actual data range

## Output Columns
- DateRange: "Jan 01, 2023 - Current" 
- PartNum: Item part number
- Description: Item description
- Brand: Item brand (MTU)
- TotalQtySold: Sum of quantities across all qualifying orders
- TaskIDs_Qty_Companies: Aggregated list showing "TaskID (Qty: X) (Company Name)"