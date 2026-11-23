# PR 3a: Feature 4 Acceptance Tests - Core Scenarios

## Summary
Automated acceptance tests validating the complete Feature 1-3 integration for 5 core scenarios.

## Test File
- **acceptance_test_feature4_core.py** (163 lines)

## Scenarios Tested

### 1. Normal Case (Full Workflow)
- Create 9 products, 7 relationships (two connected components + bridge)
- Verify: `GET /products`, `/relationships`, `/graph/info`
- Explore: `GET /explore/bfs`, `/dfs`, `/reachability`, `/components`
- Recommendations: `GET /recommendations/P001`, `/recommendations/P002`
- Assertions: Response structure, data completeness, reachable products found

### 2. Isolated Product
- Single product with zero relationships
- BFS/DFS/Reachability return 0 results
- Recommendations return 0 proposals with "no genera propuesta" message
- Components shows 1 isolated component

### 3. Non-Existent Product (404 Errors)
- `GET /products/P999`
- `GET /explore/bfs|dfs|reachability/P999`
- `GET /recommendations/P999`
- `POST /relationships` with missing product
- All return 404

### 4. Empty Graph
- Zero products, zero relationships
- All list endpoints return count=0
- `/graph/info` returns empty arrays
- `/components` returns 0 components
- `/recommendations` on missing product returns 404
- Single product in empty graph → 0 proposals

### 5. Invalid Data (400/409 Errors)
| Test | Expected | Description |
|------|----------|-------------|
| Duplicate product ID | 409 | Conflict |
| Duplicate relationship | 400 | Bad request |
| Self-relationship (A-A) | 400 | Invalid |
| Weight = 0 | 400 | Out of range (0,1] |
| Weight > 1 (1.5) | 400 | Out of range |
| Weight < 0 (-0.1) | 400 | Out of range |
| Weight = "text" | 400 | Type error |
| Product missing name | 400 | Missing field |
| Product missing ID | 400 | Missing field |
| Relationship missing fields | 400 | Missing field |
| Depth = 0 | 400 | Invalid param |
| Depth = -1 | 400 | Invalid param |

## Running Tests
```bash
# Start API first
python api.py

# In another terminal
python acceptance_test_feature4_core.py
```

## Expected Output
```
Feature 4 Acceptance - CORE Scenarios
============================================================
1. NORMAL: Full workflow
✓ PASS List products
...
5. INVALID DATA
✗ FAIL Duplicate ID
...
============================================================
CORE: 42/42 passed
🎉 Todas las pruebas CORE de Feature 4 pasaron!
```

## Test Count
- **Total**: ~42 assertions across 5 scenarios
- **Lines**: 163 (well under 400 limit)