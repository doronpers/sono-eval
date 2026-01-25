# Implementation Guide: Area 3 - Error Recovery & Troubleshooting Experience

**Parent Document:** [UX_ENHANCEMENT_ANALYSIS.md](UX_ENHANCEMENT_ANALYSIS.md)  
**Target:** Error Recovery & Troubleshooting Experience  
**Priority:** P2  
**Estimated Effort:** Medium (2-3 weeks)  
**For:** Coding Agents

---

## Overview

This guide provides step-by-step instructions for implementing enhanced error recovery and troubleshooting experiences across all Sono-Eval interfaces.

### Goals
1. Reduce error resolution time from 5-15 min to 1-3 min (-70%)
2. Achieve 80%+ self-service success rate
3. Reduce error-related support tickets by 40%
4. Lower abandonment rate on error to <10%
5. Provide actionable next steps for every error

---

## Phase 1: Enhanced Error Response Format (Priority: HIGHEST)

### Task 1.1: Extend Error Models

**Objective:** Add troubleshooting guidance to all error responses

**Files to Modify:**
- `src/sono_eval/utils/errors.py`
- `src/sono_eval/utils/error_help.py`

**Implementation:**

1. **Extend Error Models**
   ```python
   # src/sono_eval/utils/errors.py
   """Enhanced error models with troubleshooting."""
   
   from typing import List, Optional, Dict, Any
   from pydantic import BaseModel, Field
   
   
   class QuickFix(BaseModel):
       """Suggested quick fix for an error."""
       action: str  # e.g., "auto_sanitize", "retry", "check_config"
       suggestion: Optional[str] = None  # Specific value to use
       command: Optional[str] = None  # Command to run
       description: str  # What this fix does
   
   
   class TroubleshootingGuide(BaseModel):
       """Troubleshooting information."""
       common_causes: List[str] = Field(default_factory=list)
       next_steps: List[str] = Field(default_factory=list)
       prevention_tips: List[str] = Field(default_factory=list)
   
   
   class ErrorHelp(BaseModel):
       """Help information for an error."""
       field: Optional[str] = None
       example: Optional[Dict[str, Any]] = None
       docs_url: Optional[str] = None
       video_tutorial: Optional[str] = None
       related_errors: List[str] = Field(default_factory=list)
   
   
   class EnhancedErrorResponse(BaseModel):
       """Enhanced error response with troubleshooting."""
       error_code: str
       message: str
       severity: str = "error"  # "error", "warning", "info"
       quick_fix: Optional[QuickFix] = None
       troubleshooting: Optional[TroubleshootingGuide] = None
       help: Optional[ErrorHelp] = None
       timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
       request_id: Optional[str] = None
   
   
   # Base error class with enhanced response
   class SonoEvalError(Exception):
       """Base error with enhanced information."""
       
       def __init__(
           self,
           message: str,
           error_code: str = "UNKNOWN_ERROR",
           severity: str = "error",
           quick_fix: Optional[QuickFix] = None,
           troubleshooting: Optional[TroubleshootingGuide] = None,
           help: Optional[ErrorHelp] = None,
       ):
           super().__init__(message)
           self.error_code = error_code
           self.message = message
           self.severity = severity
           self.quick_fix = quick_fix
           self.troubleshooting = troubleshooting
           self.help = help
       
       def to_response(self, request_id: Optional[str] = None) -> EnhancedErrorResponse:
           """Convert to enhanced error response."""
           return EnhancedErrorResponse(
               error_code=self.error_code,
               message=self.message,
               severity=self.severity,
               quick_fix=self.quick_fix,
               troubleshooting=self.troubleshooting,
               help=self.help,
               request_id=request_id,
           )
   ```

2. **Create Error Registry**
   ```python
   # src/sono_eval/utils/error_registry.py
   """Registry of common errors with troubleshooting."""
   
   from typing import Dict
   from .errors import QuickFix, TroubleshootingGuide, ErrorHelp
   
   
   ERROR_REGISTRY: Dict[str, dict] = {
       "VALIDATION_ERROR_CANDIDATE_ID": {
           "quick_fix": QuickFix(
               action="auto_sanitize",
               suggestion="john_doe_123",
               command="sono-eval candidate create --id {sanitized_id}",
               description="Replace special characters with underscores",
           ),
           "troubleshooting": TroubleshootingGuide(
               common_causes=[
                   "Special characters (!, @, #) in candidate ID",
                   "Spaces instead of underscores",
                   "Using email address as ID",
               ],
               next_steps=[
                   "1. Use only letters, numbers, dashes, and underscores",
                   "2. Replace spaces with underscores or dashes",
                   "3. Keep ID under 50 characters",
                   "4. Retry with valid ID",
               ],
               prevention_tips=[
                   "Use format: firstname_lastname_123",
                   "Avoid special characters",
                   "Test with: sono-eval candidate validate --id <id>",
               ],
           ),
           "help": ErrorHelp(
               field="candidate_id",
               example={"candidate_id": "john_doe_123"},
               docs_url="/docs/guides/candidates#id-format",
               video_tutorial="/tutorials/candidate-creation",
               related_errors=["CANDIDATE_NOT_FOUND", "INVALID_FORMAT"],
           ),
       },
       
       "PORT_IN_USE": {
           "quick_fix": QuickFix(
               action="use_alternative_port",
               suggestion="8001",
               command="./launcher.sh start --port 8001",
               description="Start server on alternative port",
           ),
           "troubleshooting": TroubleshootingGuide(
               common_causes=[
                   "Another Sono-Eval instance is running",
                   "Different service using port 8000",
                   "Previous instance didn't shut down cleanly",
               ],
               next_steps=[
                   "1. Check what's using port: lsof -i :8000",
                   "2. Stop other instance: ./launcher.sh stop",
                   "3. Or use different port: ./launcher.sh start --port 8001",
               ],
               prevention_tips=[
                   "Always use ./launcher.sh stop before restarting",
                   "Set custom port in .env: API_PORT=8001",
                   "Use Docker to avoid port conflicts",
               ],
           ),
           "help": ErrorHelp(
               docs_url="/docs/guides/troubleshooting#port-conflicts",
               related_errors=["ADDRESS_IN_USE", "BIND_ERROR"],
           ),
       },
       
       "REDIS_CONNECTION_FAILED": {
           "quick_fix": QuickFix(
               action="start_redis",
               command="docker-compose up -d redis",
               description="Start Redis container",
           ),
           "troubleshooting": TroubleshootingGuide(
               common_causes=[
                   "Redis server not running",
                   "Wrong Redis host/port in config",
                   "Redis authentication failed",
                   "Firewall blocking Redis port",
               ],
               next_steps=[
                   "1. Check Redis status: docker ps | grep redis",
                   "2. Start Redis: docker-compose up -d redis",
                   "3. Verify connection: redis-cli ping",
                   "4. Check .env: REDIS_URL=redis://localhost:6379",
               ],
               prevention_tips=[
                   "Use Docker Compose for Redis",
                   "Set REDIS_URL in .env",
                   "Enable Redis health checks",
               ],
           ),
           "help": ErrorHelp(
               docs_url="/docs/guides/production-deployment#redis-setup",
               related_errors=["CACHE_ERROR", "RATE_LIMIT_ERROR"],
           ),
       },
       
       "MODEL_DOWNLOAD_TIMEOUT": {
           "quick_fix": QuickFix(
               action="retry_with_timeout",
               command="sono-eval setup models --timeout 300",
               description="Retry with longer timeout (5 minutes)",
           ),
           "troubleshooting": TroubleshootingGuide(
               common_causes=[
                   "Slow internet connection",
                   "Hugging Face servers busy",
                   "Firewall blocking download",
                   "Insufficient disk space",
               ],
               next_steps=[
                   "1. Check internet: ping huggingface.co",
                   "2. Check disk space: df -h",
                   "3. Increase timeout: --timeout 600",
                   "4. Or download manually and place in models/",
               ],
               prevention_tips=[
                   "Pre-download models during setup",
                   "Use cached models directory",
                   "Set HF_HOME environment variable",
               ],
           ),
           "help": ErrorHelp(
               docs_url="/docs/guides/ml-models#download-troubleshooting",
               related_errors=["MODEL_LOAD_ERROR", "NETWORK_ERROR"],
           ),
       },
       
       "ASSESSMENT_FAILED": {
           "quick_fix": QuickFix(
               action="check_logs",
               command="tail -f logs/sono-eval.log",
               description="Check detailed error logs",
           ),
           "troubleshooting": TroubleshootingGuide(
               common_causes=[
                   "Unsupported file type",
                   "File too large (>10MB)",
                   "Invalid code syntax",
                   "ML model not loaded",
               ],
               next_steps=[
                   "1. Check file size: ls -lh <file>",
                   "2. Validate code syntax",
                   "3. Check logs: tail -f logs/sono-eval.log",
                   "4. Try with simpler code first",
               ],
               prevention_tips=[
                   "Use supported languages: Python, JS, Java, Go",
                   "Keep files under 10MB",
                   "Validate syntax before submitting",
               ],
           ),
           "help": ErrorHelp(
               docs_url="/docs/guides/troubleshooting#assessment-failures",
               related_errors=["INVALID_CODE", "TIMEOUT_ERROR"],
           ),
       },
   }
   
   
   def get_error_details(error_code: str) -> dict:
       """Get enhanced error details from registry."""
       return ERROR_REGISTRY.get(error_code, {})
   ```

3. **Update Error Handler Middleware**
   ```python
   # src/sono_eval/api/middleware.py
   """Error handling middleware with enhanced responses."""
   
   from fastapi import Request, status
   from fastapi.responses import JSONResponse
   import traceback
   import uuid
   
   from sono_eval.utils.errors import SonoEvalError, EnhancedErrorResponse
   from sono_eval.utils.error_registry import get_error_details
   
   
   async def error_handler_middleware(request: Request, call_next):
       """Enhanced error handling middleware."""
       request_id = str(uuid.uuid4())
       request.state.request_id = request_id
       
       try:
           response = await call_next(request)
           return response
       
       except SonoEvalError as e:
           # Known error with troubleshooting
           error_response = e.to_response(request_id=request_id)
           
           return JSONResponse(
               status_code=status.HTTP_400_BAD_REQUEST,
               content=error_response.model_dump(),
           )
       
       except ValueError as e:
           # Validation error - enrich with troubleshooting
           error_code = "VALIDATION_ERROR"
           error_details = get_error_details(error_code)
           
           error_response = EnhancedErrorResponse(
               error_code=error_code,
               message=str(e),
               severity="warning",
               quick_fix=error_details.get("quick_fix"),
               troubleshooting=error_details.get("troubleshooting"),
               help=error_details.get("help"),
               request_id=request_id,
           )
           
           return JSONResponse(
               status_code=status.HTTP_400_BAD_REQUEST,
               content=error_response.model_dump(),
           )
       
       except Exception as e:
           # Unknown error - provide generic troubleshooting
           error_response = EnhancedErrorResponse(
               error_code="INTERNAL_ERROR",
               message="An unexpected error occurred",
               severity="error",
               troubleshooting=TroubleshootingGuide(
                   common_causes=[
                       "Temporary service issue",
                       "Invalid request format",
                       "Resource unavailable",
                   ],
                   next_steps=[
                       "1. Check service status: GET /api/v1/health",
                       "2. Review request format",
                       "3. Retry in a few seconds",
                       "4. If persists, contact support with request_id",
                   ],
               ),
               help=ErrorHelp(
                   docs_url="/docs/guides/troubleshooting",
               ),
               request_id=request_id,
           )
           
           # Log full error for debugging
           logger.error(
               f"Unhandled error: {str(e)}\n"
               f"Request ID: {request_id}\n"
               f"Traceback: {traceback.format_exc()}"
           )
           
           return JSONResponse(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               content=error_response.model_dump(),
           )
   ```

**Validation:**
```bash
# Test error responses
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": "invalid@id"}'

# Expected: Enhanced error with quick_fix, troubleshooting, help
```

---

## Phase 2: Interactive Error Recovery (Web UI) (Priority: HIGH)

### Task 2.1: Create Error Modal Component

**Objective:** Show actionable error dialogs in Web UI

**Files to Create:**
- `frontend/components/Error/ErrorModal.tsx`
- `frontend/components/Error/QuickFixButton.tsx`

**Implementation:**

1. **Create Error Modal**
   ```typescript
   // frontend/components/Error/ErrorModal.tsx
   import React, { useState } from 'react';
   import {
     Dialog,
     DialogTitle,
     DialogContent,
     DialogActions,
     Button,
     Tabs,
     Tab,
     Box,
     Alert,
     Typography,
   } from '@mui/material';
   import { QuickFixButton } from './QuickFixButton';
   
   interface ErrorModalProps {
     open: boolean;
     error: any; // EnhancedErrorResponse
     onClose: () => void;
     onRetry?: () => void;
   }
   
   export function ErrorModal({ open, error, onClose, onRetry }: ErrorModalProps) {
     const [tab, setTab] = useState(0);
     
     if (!error) return null;
     
     return (
       <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
         <DialogTitle>
           <div className="flex items-center gap-2">
             {error.severity === 'error' && '❌'}
             {error.severity === 'warning' && '⚠️'}
             {error.severity === 'info' && 'ℹ️'}
             <span>{error.error_code}</span>
           </div>
         </DialogTitle>
         
         <DialogContent>
           <Alert severity={error.severity === 'error' ? 'error' : 'warning'}>
             {error.message}
           </Alert>
           
           <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2 }}>
             <Tabs value={tab} onChange={(_, v) => setTab(v)}>
               <Tab label="Solution" />
               <Tab label="Troubleshooting" />
               <Tab label="Learn More" />
             </Tabs>
           </Box>
           
           {/* Tab 1: Solution */}
           {tab === 0 && (
             <Box sx={{ p: 2 }}>
               {error.quick_fix && (
                 <>
                   <Typography variant="h6" gutterBottom>
                     Quick Fix
                   </Typography>
                   
                   <Typography variant="body2" paragraph>
                     {error.quick_fix.description}
                   </Typography>
                   
                   {error.quick_fix.suggestion && (
                     <div className="bg-gray-100 p-3 rounded mb-4">
                       <strong>Suggested value:</strong>{' '}
                       <code>{error.quick_fix.suggestion}</code>
                     </div>
                   )}
                   
                   {error.quick_fix.command && (
                     <div className="bg-gray-100 p-3 rounded mb-4">
                       <strong>Run this command:</strong>
                       <pre className="mt-2 font-mono text-sm">
                         {error.quick_fix.command}
                       </pre>
                       <QuickFixButton
                         action={error.quick_fix.action}
                         command={error.quick_fix.command}
                         suggestion={error.quick_fix.suggestion}
                       />
                     </div>
                   )}
                 </>
               )}
               
               {error.help?.example && (
                 <>
                   <Typography variant="h6" gutterBottom>
                     Example
                   </Typography>
                   <pre className="bg-gray-100 p-3 rounded text-sm">
                     {JSON.stringify(error.help.example, null, 2)}
                   </pre>
                 </>
               )}
             </Box>
           )}
           
           {/* Tab 2: Troubleshooting */}
           {tab === 1 && error.troubleshooting && (
             <Box sx={{ p: 2 }}>
               {error.troubleshooting.common_causes.length > 0 && (
                 <>
                   <Typography variant="h6" gutterBottom>
                     Common Causes
                   </Typography>
                   <ul>
                     {error.troubleshooting.common_causes.map((cause, i) => (
                       <li key={i}>{cause}</li>
                     ))}
                   </ul>
                 </>
               )}
               
               {error.troubleshooting.next_steps.length > 0 && (
                 <>
                   <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                     Next Steps
                   </Typography>
                   <ol>
                     {error.troubleshooting.next_steps.map((step, i) => (
                       <li key={i}>{step}</li>
                     ))}
                   </ol>
                 </>
               )}
               
               {error.troubleshooting.prevention_tips.length > 0 && (
                 <>
                   <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                     Prevention Tips
                   </Typography>
                   <ul>
                     {error.troubleshooting.prevention_tips.map((tip, i) => (
                       <li key={i}>{tip}</li>
                     ))}
                   </ul>
                 </>
               )}
             </Box>
           )}
           
           {/* Tab 3: Learn More */}
           {tab === 2 && error.help && (
             <Box sx={{ p: 2 }}>
               {error.help.docs_url && (
                 <div className="mb-4">
                   <Typography variant="h6" gutterBottom>
                     Documentation
                   </Typography>
                   <a
                     href={error.help.docs_url}
                     target="_blank"
                     rel="noopener noreferrer"
                     className="text-blue-500 hover:underline"
                   >
                     Read the docs →
                   </a>
                 </div>
               )}
               
               {error.help.video_tutorial && (
                 <div className="mb-4">
                   <Typography variant="h6" gutterBottom>
                     Video Tutorial
                   </Typography>
                   <a
                     href={error.help.video_tutorial}
                     target="_blank"
                     rel="noopener noreferrer"
                     className="text-blue-500 hover:underline"
                   >
                     Watch tutorial →
                   </a>
                 </div>
               )}
               
               {error.help.related_errors && error.help.related_errors.length > 0 && (
                 <div>
                   <Typography variant="h6" gutterBottom>
                     Related Errors
                   </Typography>
                   <ul>
                     {error.help.related_errors.map((code, i) => (
                       <li key={i}>
                         <a
                           href={`/docs/errors#${code}`}
                           className="text-blue-500 hover:underline"
                         >
                           {code}
                         </a>
                       </li>
                     ))}
                   </ul>
                 </div>
               )}
               
               <div className="mt-4 p-3 bg-blue-50 rounded">
                 <Typography variant="body2">
                   <strong>Request ID:</strong> {error.request_id}
                 </Typography>
                 <Typography variant="caption" display="block">
                   Include this when contacting support
                 </Typography>
               </div>
             </Box>
           )}
         </DialogContent>
         
         <DialogActions>
           <Button onClick={onClose}>Close</Button>
           {onRetry && (
             <Button onClick={onRetry} variant="contained" color="primary">
               Retry
             </Button>
           )}
         </DialogActions>
       </Dialog>
     );
   }
   ```

2. **Create Quick Fix Button**
   ```typescript
   // frontend/components/Error/QuickFixButton.tsx
   import React, { useState } from 'react';
   import { Button, CircularProgress } from '@mui/material';
   
   interface QuickFixButtonProps {
     action: string;
     command?: string;
     suggestion?: string;
   }
   
   export function QuickFixButton({ action, command, suggestion }: QuickFixButtonProps) {
     const [loading, setLoading] = useState(false);
     const [applied, setApplied] = useState(false);
     
     const handleApply = async () => {
       setLoading(true);
       
       try {
         // Different actions
         switch (action) {
           case 'auto_sanitize':
             // Apply sanitized value
             if (suggestion) {
               // Update form with sanitized value
               // (Specific to context where error occurred)
               console.log('Applying sanitized value:', suggestion);
             }
             break;
           
           case 'retry':
             // Retry failed operation
             console.log('Retrying operation...');
             break;
           
           case 'copy_command':
             // Copy command to clipboard
             if (command) {
               await navigator.clipboard.writeText(command);
             }
             break;
         }
         
         setApplied(true);
         setTimeout(() => setApplied(false), 2000);
       } catch (error) {
         console.error('Quick fix failed:', error);
       } finally {
         setLoading(false);
       }
     };
     
     return (
       <Button
         variant="contained"
         color="primary"
         onClick={handleApply}
         disabled={loading || applied}
         startIcon={loading && <CircularProgress size={16} />}
       >
         {loading ? 'Applying...' : applied ? 'Applied ✓' : 'Apply Fix'}
       </Button>
     );
   }
   ```

3. **Integrate with API Calls**
   ```typescript
   // frontend/lib/api.ts
   import { ErrorModal } from '@/components/Error/ErrorModal';
   
   export async function apiCall(endpoint: string, options: RequestInit) {
     try {
       const response = await fetch(endpoint, options);
       
       if (!response.ok) {
         const errorData = await response.json();
         
         // Show error modal
         // (Use context or state management to show modal globally)
         showErrorModal(errorData);
         
         throw new Error(errorData.message);
       }
       
       return response.json();
     } catch (error) {
       console.error('API call failed:', error);
       throw error;
     }
   }
   ```

**Validation:**
- Trigger validation error: Should show modal with 3 tabs
- Click "Apply Fix": Should auto-correct value
- Click "Read docs": Should open documentation
- Check request ID shown: Should be included

---

## Phase 3: Smart Error Prevention (Priority: MEDIUM)

### Task 3.1: Add Pre-Validation

**Objective:** Catch errors before API calls

**Files to Create:**
- `frontend/lib/validation.ts`
- `frontend/hooks/useValidation.ts`

**Implementation:**

1. **Create Validation Library**
   ```typescript
   // frontend/lib/validation.ts
   
   export interface ValidationResult {
     valid: boolean;
     errors: string[];
     warnings: string[];
     suggestions: Record<string, string>;
   }
   
   export function validateCandidateId(id: string): ValidationResult {
     const result: ValidationResult = {
       valid: true,
       errors: [],
       warnings: [],
       suggestions: {},
     };
     
     // Check format
     if (!/^[a-zA-Z0-9_-]+$/.test(id)) {
       result.valid = false;
       result.errors.push('ID must contain only letters, numbers, dash, and underscore');
       
       // Auto-sanitize suggestion
       const sanitized = id.replace(/[^a-zA-Z0-9_-]/g, '_');
       result.suggestions.candidate_id = sanitized;
     }
     
     // Check length
     if (id.length > 50) {
       result.valid = false;
       result.errors.push('ID must be 50 characters or less');
     }
     
     if (id.length < 3) {
       result.warnings.push('ID is very short. Consider using something more descriptive');
     }
     
     return result;
   }
   
   export function validateCode(code: string, language: string): ValidationResult {
     const result: ValidationResult = {
       valid: true,
       errors: [],
       warnings: [],
       suggestions: {},
     };
     
     // Check size
     if (code.length > 1024 * 1024 * 10) {
       result.valid = false;
       result.errors.push('Code is too large (max 10MB)');
     }
     
     // Basic syntax check (very simple)
     if (language === 'python') {
       const lines = code.split('\n');
       for (let i = 0; i < lines.length; i++) {
         if (lines[i].includes('def ') && !lines[i].endsWith(':')) {
           result.warnings.push(`Line ${i + 1}: Missing colon after function definition`);
         }
       }
     }
     
     return result;
   }
   ```

2. **Create Validation Hook**
   ```typescript
   // frontend/hooks/useValidation.ts
   import { useState, useEffect } from 'react';
   import { ValidationResult, validateCandidateId, validateCode } from '@/lib/validation';
   
   export function useValidation(field: string, value: string, language?: string) {
     const [validation, setValidation] = useState<ValidationResult>({
       valid: true,
       errors: [],
       warnings: [],
       suggestions: {},
     });
     
     useEffect(() => {
       // Debounce validation
       const timer = setTimeout(() => {
         let result: ValidationResult;
         
         switch (field) {
           case 'candidate_id':
             result = validateCandidateId(value);
             break;
           case 'code':
             result = validateCode(value, language || 'python');
             break;
           default:
             result = { valid: true, errors: [], warnings: [], suggestions: {} };
         }
         
         setValidation(result);
       }, 500);
       
       return () => clearTimeout(timer);
     }, [field, value, language]);
     
     return validation;
   }
   ```

3. **Use in Form**
   ```typescript
   // frontend/components/AssessmentForm.tsx
   import { useValidation } from '@/hooks/useValidation';
   
   export function AssessmentForm() {
     const [candidateId, setCandidateId] = useState('');
     const validation = useValidation('candidate_id', candidateId);
     
     const handleApplySuggestion = () => {
       if (validation.suggestions.candidate_id) {
         setCandidateId(validation.suggestions.candidate_id);
       }
     };
     
     return (
       <form>
         <TextField
           label="Candidate ID"
           value={candidateId}
           onChange={(e) => setCandidateId(e.target.value)}
           error={!validation.valid}
           helperText={
             <>
               {validation.errors.map((err, i) => (
                 <div key={i} className="text-red-500">{err}</div>
               ))}
               {validation.warnings.map((warn, i) => (
                 <div key={i} className="text-yellow-600">{warn}</div>
               ))}
               {validation.suggestions.candidate_id && (
                 <div className="mt-2">
                   <strong>Suggestion:</strong> {validation.suggestions.candidate_id}
                   <Button size="small" onClick={handleApplySuggestion}>
                     Apply
                   </Button>
                 </div>
               )}
             </>
           }
         />
       </form>
     );
   }
   ```

**Validation:**
- Type invalid ID: Should show error + suggestion in real-time
- Click "Apply": Should auto-correct input
- Submit form: Should prevent submission if invalid

---

## Phase 4: Error History & Learning (Priority: MEDIUM)

### Task 4.1: Create Error History Dashboard

**Objective:** Track errors and learn from patterns

**Files to Create:**
- `frontend/app/errors/page.tsx`
- `src/sono_eval/utils/error_tracker.py`

**Implementation:**

1. **Error Tracker (Backend)**
   ```python
   # src/sono_eval/utils/error_tracker.py
   """Track and analyze error patterns."""
   
   import json
   from pathlib import Path
   from datetime import datetime
   from typing import List, Dict
   from collections import Counter
   
   
   class ErrorTracker:
       """Track errors for analysis."""
       
       def __init__(self, storage_path: str = "./data/errors"):
           self.storage_path = Path(storage_path)
           self.storage_path.mkdir(parents=True, exist_ok=True)
       
       def log_error(self, error_data: dict) -> None:
           """Log an error occurrence."""
           error_file = self.storage_path / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
           
           with open(error_file, 'a') as f:
               f.write(json.dumps(error_data) + '\n')
       
       def get_recent_errors(self, days: int = 7) -> List[dict]:
           """Get errors from last N days."""
           errors = []
           
           for i in range(days):
               date = datetime.now() - timedelta(days=i)
               error_file = self.storage_path / f"{date.strftime('%Y-%m-%d')}.jsonl"
               
               if error_file.exists():
                   with open(error_file, 'r') as f:
                       for line in f:
                           errors.append(json.loads(line))
           
           return errors
       
       def get_error_stats(self, days: int = 7) -> Dict:
           """Get error statistics."""
           errors = self.get_recent_errors(days)
           
           # Count by error code
           error_codes = Counter(e['error_code'] for e in errors)
           
           # Count by user
           users = Counter(e.get('user_id', 'unknown') for e in errors)
           
           # Count resolved
           resolved = sum(1 for e in errors if e.get('resolved', False))
           
           return {
               'total_errors': len(errors),
               'unique_codes': len(error_codes),
               'top_errors': dict(error_codes.most_common(10)),
               'affected_users': len(users),
               'resolved_count': resolved,
               'resolution_rate': resolved / len(errors) if errors else 0,
           }
   ```

2. **Error History Page (Frontend)**
   ```typescript
   // frontend/app/errors/page.tsx
   'use client';
   
   import React, { useEffect, useState } from 'react';
   import {
     Card,
     CardContent,
     Typography,
     Table,
     TableBody,
     TableCell,
     TableHead,
     TableRow,
     Chip,
   } from '@mui/material';
   
   export default function ErrorHistoryPage() {
     const [stats, setStats] = useState<any>(null);
     const [errors, setErrors] = useState<any[]>([]);
     
     useEffect(() => {
       fetchErrorStats();
       fetchRecentErrors();
     }, []);
     
     const fetchErrorStats = async () => {
       const response = await fetch('/api/v1/errors/stats');
       const data = await response.json();
       setStats(data);
     };
     
     const fetchRecentErrors = async () => {
       const response = await fetch('/api/v1/errors/recent');
       const data = await response.json();
       setErrors(data);
     };
     
     return (
       <div className="p-8">
         <Typography variant="h4" gutterBottom>
           Error History
         </Typography>
         
         {/* Stats Overview */}
         <div className="grid grid-cols-4 gap-4 mb-8">
           <Card>
             <CardContent>
               <Typography color="textSecondary" gutterBottom>
                 Total Errors
               </Typography>
               <Typography variant="h5">
                 {stats?.total_errors || 0}
               </Typography>
             </CardContent>
           </Card>
           
           <Card>
             <CardContent>
               <Typography color="textSecondary" gutterBottom>
                 Unique Error Types
               </Typography>
               <Typography variant="h5">
                 {stats?.unique_codes || 0}
               </Typography>
             </CardContent>
           </Card>
           
           <Card>
             <CardContent>
               <Typography color="textSecondary" gutterBottom>
                 Resolved
               </Typography>
               <Typography variant="h5">
                 {stats?.resolved_count || 0}
               </Typography>
             </CardContent>
           </Card>
           
           <Card>
             <CardContent>
               <Typography color="textSecondary" gutterBottom>
                 Resolution Rate
               </Typography>
               <Typography variant="h5">
                 {((stats?.resolution_rate || 0) * 100).toFixed(0)}%
               </Typography>
             </CardContent>
           </Card>
         </div>
         
         {/* Top Errors */}
         <Card className="mb-8">
           <CardContent>
             <Typography variant="h6" gutterBottom>
               Most Common Errors
             </Typography>
             <Table>
               <TableHead>
                 <TableRow>
                   <TableCell>Error Code</TableCell>
                   <TableCell align="right">Count</TableCell>
                 </TableRow>
               </TableHead>
               <TableBody>
                 {stats?.top_errors && Object.entries(stats.top_errors).map(([code, count]) => (
                   <TableRow key={code}>
                     <TableCell>{code}</TableCell>
                     <TableCell align="right">{count as number}</TableCell>
                   </TableRow>
                 ))}
               </TableBody>
             </Table>
           </CardContent>
         </Card>
         
         {/* Recent Errors */}
         <Card>
           <CardContent>
             <Typography variant="h6" gutterBottom>
               Recent Errors
             </Typography>
             <Table>
               <TableHead>
                 <TableRow>
                   <TableCell>Time</TableCell>
                   <TableCell>Error Code</TableCell>
                   <TableCell>Message</TableCell>
                   <TableCell>Status</TableCell>
                   <TableCell>Actions</TableCell>
                 </TableRow>
               </TableHead>
               <TableBody>
                 {errors.map((error, i) => (
                   <TableRow key={i}>
                     <TableCell>
                       {new Date(error.timestamp).toLocaleString()}
                     </TableCell>
                     <TableCell>{error.error_code}</TableCell>
                     <TableCell>{error.message}</TableCell>
                     <TableCell>
                       <Chip
                         label={error.resolved ? 'Resolved' : 'Open'}
                         color={error.resolved ? 'success' : 'warning'}
                         size="small"
                       />
                     </TableCell>
                     <TableCell>
                       <button
                         className="text-blue-500 hover:underline"
                         onClick={() => {/* Show error details */}}
                       >
                         View
                       </button>
                     </TableCell>
                   </TableRow>
                 ))}
               </TableBody>
             </Table>
           </CardContent>
         </Card>
       </div>
     );
   }
   ```

**Validation:**
- Generate some errors: Run invalid API calls
- Check error history page: Should show stats and recent errors
- Mark error as resolved: Should update resolution rate

---

## Phase 5: CLI "Fix It For Me" Command (Priority: MEDIUM)

### Task 5.1: Create Diagnostic CLI Command

**Objective:** Auto-diagnose and fix common issues

**Files to Create:**
- `src/sono_eval/cli/commands/diagnose.py`

**Implementation:**

1. **Create Diagnose Command**
   ```python
   # src/sono_eval/cli/commands/diagnose.py
   """Diagnostic commands."""
   
   import click
   import subprocess
   import socket
   from rich.console import Console
   from rich.panel import Panel
   from rich.progress import Progress
   
   console = Console()
   
   
   @click.group()
   def diagnose():
       """Diagnose and fix common issues."""
       pass
   
   
   @diagnose.command()
   def system():
       """Check system requirements and configuration."""
       console.print(Panel.fit("🔍 Running System Diagnostics", style="bold blue"))
       
       checks = [
           ("Python Version", check_python_version),
           ("Docker", check_docker),
           ("Port 8000", check_port),
           ("Redis", check_redis),
           (".env File", check_env_file),
           ("Storage Directories", check_storage),
       ]
       
       results = []
       
       with Progress() as progress:
           task = progress.add_task("Running checks...", total=len(checks))
           
           for name, check_fn in checks:
               result = check_fn()
               results.append((name, result))
               progress.update(task, advance=1)
       
       # Display results
       console.print("\n[bold]Diagnostic Results:[/bold]\n")
       
       for name, result in results:
           status = "✅" if result['ok'] else "❌"
           console.print(f"{status} {name}: {result['message']}")
           
           if not result['ok'] and result.get('fix'):
               console.print(f"   💡 Fix: {result['fix']}", style="yellow")
       
       # Offer to auto-fix
       issues = [r for r in results if not r[1]['ok'] and r[1].get('auto_fix')]
       
       if issues:
           console.print(f"\n[bold yellow]Found {len(issues)} fixable issues[/bold yellow]")
           if click.confirm("Apply automatic fixes?"):
               for name, result in issues:
                   console.print(f"Fixing: {name}...")
                   result['auto_fix']()
   
   
   def check_python_version():
       """Check Python version."""
       import sys
       version = sys.version_info
       
       if version.major == 3 and version.minor >= 12:
           return {'ok': True, 'message': f"Python {version.major}.{version.minor}"}
       else:
           return {
               'ok': False,
               'message': f"Python {version.major}.{version.minor} (need 3.12+)",
               'fix': "Upgrade Python to 3.12 or higher",
           }
   
   
   def check_docker():
       """Check if Docker is running."""
       try:
           subprocess.run(['docker', 'ps'], capture_output=True, check=True)
           return {'ok': True, 'message': "Running"}
       except (subprocess.CalledProcessError, FileNotFoundError):
           return {
               'ok': False,
               'message': "Not running or not installed",
               'fix': "Start Docker: docker-compose up -d",
           }
   
   
   def check_port():
       """Check if port 8000 is available."""
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       result = sock.connect_ex(('localhost', 8000))
       sock.close()
       
       if result != 0:
           return {'ok': True, 'message': "Available"}
       else:
           return {
               'ok': False,
               'message': "Port 8000 in use",
               'fix': "Stop service: ./launcher.sh stop, or use --port 8001",
           }
   
   
   def check_redis():
       """Check if Redis is accessible."""
       try:
           import redis
           r = redis.Redis(host='localhost', port=6379)
           r.ping()
           return {'ok': True, 'message': "Connected"}
       except Exception:
           return {
               'ok': False,
               'message': "Cannot connect",
               'fix': "Start Redis: docker-compose up -d redis",
               'auto_fix': lambda: subprocess.run(['docker-compose', 'up', '-d', 'redis']),
           }
   
   
   def check_env_file():
       """Check if .env file exists."""
       from pathlib import Path
       
       if Path('.env').exists():
           return {'ok': True, 'message': "Found"}
       else:
           return {
               'ok': False,
               'message': "Missing",
               'fix': "Copy .env.example to .env",
               'auto_fix': lambda: shutil.copy('.env.example', '.env'),
           }
   
   
   def check_storage():
       """Check if storage directories exist."""
       from pathlib import Path
       
       dirs = ['data/memory', 'data/tagstudio', 'models/cache']
       missing = [d for d in dirs if not Path(d).exists()]
       
       if not missing:
           return {'ok': True, 'message': "All directories exist"}
       else:
           return {
               'ok': False,
               'message': f"Missing: {', '.join(missing)}",
               'fix': f"Create: mkdir -p {' '.join(missing)}",
               'auto_fix': lambda: [Path(d).mkdir(parents=True, exist_ok=True) for d in missing],
           }
   
   
   @diagnose.command()
   @click.option('--error-code', help='Error code to diagnose')
   def error(error_code):
       """Get help for a specific error."""
       from sono_eval.utils.error_registry import get_error_details
       
       details = get_error_details(error_code)
       
       if not details:
           console.print(f"[red]Error code '{error_code}' not found[/red]")
           return
       
       console.print(Panel.fit(f"Error: {error_code}", style="bold red"))
       
       if details.get('troubleshooting'):
           ts = details['troubleshooting']
           
           console.print("\n[bold]Common Causes:[/bold]")
           for cause in ts.get('common_causes', []):
               console.print(f"  • {cause}")
           
           console.print("\n[bold]Next Steps:[/bold]")
           for step in ts.get('next_steps', []):
               console.print(f"  {step}")
       
       if details.get('quick_fix'):
           qf = details['quick_fix']
           console.print(f"\n[bold yellow]Quick Fix:[/bold yellow] {qf['description']}")
           
           if qf.get('command'):
               console.print(f"[bold]Command:[/bold] {qf['command']}")
               
               if click.confirm("Run this command now?"):
                   subprocess.run(qf['command'], shell=True)
   ```

2. **Register Command**
   ```python
   # src/sono_eval/cli/main.py
   from sono_eval.cli.commands.diagnose import diagnose
   
   cli.add_command(diagnose)
   ```

**Validation:**
```bash
# Run diagnostics
sono-eval diagnose system

# Check specific error
sono-eval diagnose error --error-code REDIS_CONNECTION_FAILED

# Apply fixes
sono-eval diagnose system
# Answer "y" to apply fixes
```

---

## Testing & Validation

### Test Scenarios

1. **API Error Response**
   - Trigger validation error: Should return enhanced response with troubleshooting
   - Check quick_fix: Should include suggestion and command
   - Verify help links: Should point to correct docs

2. **Web UI Error Modal**
   - Trigger error in form: Should show modal with 3 tabs
   - Test tab navigation: Should show different content
   - Click "Apply Fix": Should auto-correct input
   - Click retry: Should retry failed operation

3. **Pre-Validation**
   - Type invalid input: Should show warning in real-time
   - Apply suggestion: Should auto-correct
   - Submit invalid form: Should prevent submission

4. **Error History**
   - Generate errors: Should log to backend
   - Check dashboard: Should show stats
   - Mark resolved: Should update counts

5. **CLI Diagnostics**
   - Run `diagnose system`: Should check all systems
   - Fix issues: Should apply auto-fixes
   - Check error help: Should show troubleshooting

---

## Rollout Plan

### Pre-Launch
1. Implement enhanced error models
2. Update error registry
3. Build Web UI components
4. Test all error scenarios

### Launch (Staged)
1. Week 1: Backend error responses
2. Week 2: Web UI error modals
3. Week 3: Pre-validation
4. Week 4: CLI diagnostics

### Post-Launch
1. Monitor error resolution times
2. Collect user feedback
3. Expand error registry
4. Add more quick fixes

---

## Success Metrics

### Quantitative
- Error resolution time: 1-3 min (baseline: 5-15 min)
- Self-service rate: 80%+
- Error-related support tickets: -40%
- Abandonment on error: <10%

### Qualitative
- User frustration: Low
- "Easy to fix errors" feedback: 80%+
- Support team satisfaction: High

---

## Related Documents
- [UX_ENHANCEMENT_ANALYSIS.md](UX_ENHANCEMENT_ANALYSIS.md) - Parent analysis
- [IMPLEMENTATION_GUIDE_AREA1_DOCUMENTATION.md](IMPLEMENTATION_GUIDE_AREA1_DOCUMENTATION.md) - Documentation guide
- [IMPLEMENTATION_GUIDE_AREA2_ONBOARDING.md](IMPLEMENTATION_GUIDE_AREA2_ONBOARDING.md) - Onboarding guide

---

**Version:** 1.0  
**Last Updated:** January 25, 2026  
**Status:** Ready for Implementation
