# 🧪 Testing Instructions

## Quick Test - Use Test Page

1. Open the test page in your browser:
   ```
   file:///Users/chaitanyasonar/Desktop/druggs/test_connection.html
   ```
   
   Or simply open the file `test_connection.html` in Chrome/Firefox/Safari

2. The page will automatically test:
   - ✅ Backend health check
   - ✅ Drug analysis API
   - ✅ Hugging Face medicine integration

3. Click the buttons to test different features:
   - "Test Health Endpoint" - Check if backend is running
   - "Test: Metformin for Cancer" - Test full analysis pipeline
   - "Get All Medicines" - Test Hugging Face integration
   - "Search: Metformin" - Test medicine search

## Full App Test

1. Open your browser and go to:
   ```
   http://localhost:5174
   ```

2. Try these example searches:

   ### Example 1: Metformin for Cancer
   - Drug Name: `Metformin`
   - Target Condition: `Cancer`
   - Expected Score: ~89
   - Click "Generate Repurposeability Report"

   ### Example 2: Aspirin for Cardiovascular Disease
   - Drug Name: `Aspirin`
   - Target Condition: `Cardiovascular Disease`
   - Expected Score: ~92
   - Click "Generate Repurposeability Report"

   ### Example 3: Sildenafil for Pulmonary Hypertension
   - Drug Name: `Sildenafil`
   - Target Condition: `Pulmonary Hypertension`
   - Expected Score: ~93
   - Click "Generate Repurposeability Report"

## What You Should See

### If Everything Works ✅
1. Loading animation appears
2. After 1-2 seconds, comprehensive report displays with:
   - Repurposeability Score (0-100)
   - Research Papers section
   - Clinical Trials section
   - Patents section
   - Market Feasibility section
   - Recommendations section

### If Something is Wrong ❌

#### Error: "Failed to fetch" or "Network Error"
**Solution**: Backend is not running or needs restart

```bash
# In terminal 4 (backend terminal):
# Press Ctrl+C to stop if running
cd /Users/chaitanyasonar/Desktop/druggs/backend
source venv/bin/activate
python3 main.py
```

You should see:
```
✅ Hugging Face medicine service initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Error: CORS Policy Error (in browser console)
**Solution**: Backend needs restart to load new CORS settings

The CORS configuration has been updated to allow port 5174. Restart backend:
```bash
# Press Ctrl+C in terminal 4
python3 main.py
```

#### Frontend Not Loading
**Solution**: Restart frontend

```bash
# In terminal 2 (frontend terminal):
# Press Ctrl+C to stop if running
npm run dev
```

## Verify Services Are Running

### Check Backend (Should show in terminal 4):
```
⚠️  OpenAI API key not found, using intelligent fallback system
✅ Hugging Face medicine service initialized
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Check Frontend (Should show in terminal 2):
```
VITE v5.4.21  ready in XXX ms

➜  Local:   http://localhost:5174/
➜  Network: use --host to expose
```

### Manual Verification

#### Test Backend Directly:
```bash
curl http://localhost:8000/health
```

Expected output:
```json
{"status":"healthy","ai_service":"operational"}
```

#### Test Frontend:
Open browser to `http://localhost:5174` - you should see the Drug Repurposing Platform homepage.

## Expected Flow

1. **User enters data**:
   - Drug: Metformin
   - Condition: Cancer

2. **Frontend sends request**:
   ```
   POST http://localhost:8000/api/analyze
   Body: {"drug_name": "Metformin", "target_condition": "Cancer"}
   ```

3. **Backend processes** (you'll see in terminal 4):
   ```
   INFO:     127.0.0.1:XXXXX - "POST /api/analyze HTTP/1.1" 200 OK
   ```

4. **Frontend receives and displays**:
   - Beautiful repurposeability report with all sections filled

## Debugging Tips

### Open Browser DevTools (F12):
- **Console tab**: Check for JavaScript errors or CORS errors
- **Network tab**: See the actual API requests and responses

### Check API Documentation:
Visit `http://localhost:8000/docs` for interactive Swagger UI

### Test Individual Endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Get all medicines
curl http://localhost:8000/api/medicines

# Search for a medicine
curl "http://localhost:8000/api/medicines/search?drug_name=Metformin"

# Full analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"drug_name":"Metformin","target_condition":"Cancer"}'
```

## Success Checklist

- [ ] Backend terminal shows: "✅ Hugging Face medicine service initialized"
- [ ] Backend terminal shows: "INFO:     Uvicorn running on http://0.0.0.0:8000"
- [ ] Frontend terminal shows: "Local:   http://localhost:5174/"
- [ ] Opening http://localhost:5174 shows the homepage
- [ ] `curl http://localhost:8000/health` returns {"status":"healthy"}
- [ ] Submitting a search shows loading animation
- [ ] Report displays with data after 1-2 seconds
- [ ] No CORS errors in browser console
- [ ] Backend terminal shows POST request when search submitted

## 🎉 Everything Working?

If all checkmarks above are ✅, then:

**🎊 CONGRATULATIONS! Your frontend and backend are fully connected and working together! 🎊**

Try different drug-condition combinations:
- Metformin + PCOS
- Zinc + Diarrhea  
- Thalidomide + Multiple Myeloma
- Any other combination you're interested in!

The system uses:
- ✅ Real Hugging Face medicine data
- ✅ AI-powered analysis
- ✅ Evidence-based scoring
- ✅ Medically accurate information

---

**Need More Help?** Check `CONNECTION_GUIDE.md` for detailed technical information.

