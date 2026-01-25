# Implementation Guide: Area 2 - Unified Onboarding Experience

**Parent Document:** [UX_ENHANCEMENT_ANALYSIS.md](UX_ENHANCEMENT_ANALYSIS.md)  
**Target:** Unified Onboarding Experience Across All Interfaces  
**Priority:** P1  
**Estimated Effort:** High (3-4 weeks)  
**For:** Coding Agents

---

## Overview

This guide provides step-by-step instructions for implementing a unified onboarding experience across all four Sono-Eval interfaces: CLI, API, Web UI, and Mobile.

### Goals
1. Achieve 80%+ completion rate for first assessments (Web UI)
2. Increase cross-interface adoption to 60%+
3. Reduce time-to-value to 3-5 minutes
4. Improve feature discovery to 70%+
5. Establish consistent terminology across interfaces

---

## Phase 1: Universal Onboarding Framework (Priority: HIGHEST)

### Task 1.1: Create Shared Onboarding State

**Objective:** Track onboarding progress across all interfaces

**Files to Create:**
- `src/sono_eval/onboarding/__init__.py`
- `src/sono_eval/onboarding/state.py`
- `src/sono_eval/onboarding/models.py`

**Implementation:**

1. **Define Onboarding Models**
   ```python
   # src/sono_eval/onboarding/models.py
   """Onboarding state models."""
   
   from datetime import datetime
   from typing import List, Optional
   from pydantic import BaseModel, Field
   
   
   class OnboardingStep(BaseModel):
       """Single onboarding step."""
       step_id: str
       name: str
       description: str
       completed: bool = False
       completed_at: Optional[datetime] = None
       completed_via: Optional[str] = None  # 'cli', 'api', 'web', 'mobile'
   
   
   class OnboardingState(BaseModel):
       """User onboarding state."""
       user_id: str
       started_at: datetime = Field(default_factory=datetime.now)
       completed: bool = False
       completed_at: Optional[datetime] = None
       current_step: Optional[str] = None
       
       steps: List[OnboardingStep] = Field(default_factory=lambda: [
           OnboardingStep(
               step_id="create_candidate",
               name="Create Your Profile",
               description="Set up your candidate profile"
           ),
           OnboardingStep(
               step_id="first_assessment",
               name="Run First Assessment",
               description="Complete your first code assessment"
           ),
           OnboardingStep(
               step_id="view_results",
               name="View Results",
               description="Understand your assessment results"
           ),
           OnboardingStep(
               step_id="export_data",
               name="Export Results",
               description="Download your assessment data"
           ),
           OnboardingStep(
               step_id="try_another_interface",
               name="Explore Other Interfaces",
               description="Try CLI, API, or Mobile"
           ),
       ])
       
       def mark_step_complete(self, step_id: str, interface: str) -> bool:
           """Mark a step as complete."""
           for step in self.steps:
               if step.step_id == step_id:
                   if not step.completed:
                       step.completed = True
                       step.completed_at = datetime.now()
                       step.completed_via = interface
                       
                       # Update current step
                       next_incomplete = self.get_next_step()
                       self.current_step = next_incomplete.step_id if next_incomplete else None
                       
                       # Check if all complete
                       if all(s.completed for s in self.steps):
                           self.completed = True
                           self.completed_at = datetime.now()
                       
                       return True
           return False
       
       def get_next_step(self) -> Optional[OnboardingStep]:
           """Get the next incomplete step."""
           for step in self.steps:
               if not step.completed:
                   return step
           return None
       
       def get_progress_percentage(self) -> float:
           """Calculate completion percentage."""
           completed_count = sum(1 for s in self.steps if s.completed)
           return (completed_count / len(self.steps)) * 100
   ```

2. **Create Onboarding State Manager**
   ```python
   # src/sono_eval/onboarding/state.py
   """Onboarding state management."""
   
   import json
   from pathlib import Path
   from typing import Optional
   
   from .models import OnboardingState
   
   
   class OnboardingManager:
       """Manages onboarding state persistence."""
       
       def __init__(self, storage_path: str = "./data/onboarding"):
           self.storage_path = Path(storage_path)
           self.storage_path.mkdir(parents=True, exist_ok=True)
       
       def get_state(self, user_id: str) -> OnboardingState:
           """Get onboarding state for user."""
           state_file = self.storage_path / f"{user_id}.json"
           
           if state_file.exists():
               with open(state_file, 'r') as f:
                   data = json.load(f)
               return OnboardingState(**data)
           else:
               # Create new state
               state = OnboardingState(user_id=user_id)
               self.save_state(state)
               return state
       
       def save_state(self, state: OnboardingState) -> None:
           """Save onboarding state."""
           state_file = self.storage_path / f"{state.user_id}.json"
           
           with open(state_file, 'w') as f:
               json.dump(state.model_dump(), f, indent=2, default=str)
       
       def mark_complete(self, user_id: str, step_id: str, interface: str) -> OnboardingState:
           """Mark a step as complete."""
           state = self.get_state(user_id)
           state.mark_step_complete(step_id, interface)
           self.save_state(state)
           return state
   
   
   # Global instance
   _onboarding_manager = None
   
   
   def get_onboarding_manager() -> OnboardingManager:
       """Get global onboarding manager instance."""
       global _onboarding_manager
       if _onboarding_manager is None:
           _onboarding_manager = OnboardingManager()
       return _onboarding_manager
   ```

3. **Integrate with Existing Code**
   - Add to candidate creation (CLI, API)
   - Add to assessment engine (mark "first_assessment" complete)
   - Add to results display (mark "view_results" complete)

**Validation:**
```python
# Test onboarding state
from sono_eval.onboarding import get_onboarding_manager

manager = get_onboarding_manager()
state = manager.get_state("test_user")
print(f"Progress: {state.get_progress_percentage()}%")

# Mark step complete
manager.mark_complete("test_user", "create_candidate", "cli")
state = manager.get_state("test_user")
print(f"Progress: {state.get_progress_percentage()}%")
```

---

### Task 1.2: Add Onboarding API Endpoints

**Objective:** Expose onboarding state via REST API

**Files to Modify:**
- `src/sono_eval/api/routes/__init__.py`
- Create: `src/sono_eval/api/routes/onboarding.py`

**Implementation:**

1. **Create Onboarding Routes**
   ```python
   # src/sono_eval/api/routes/onboarding.py
   """Onboarding API routes."""
   
   from fastapi import APIRouter, HTTPException, status
   from pydantic import BaseModel
   
   from sono_eval.onboarding import get_onboarding_manager, OnboardingState
   
   router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])
   
   
   class StepCompleteRequest(BaseModel):
       """Request to mark step complete."""
       step_id: str
       interface: str
   
   
   @router.get("/{user_id}", response_model=OnboardingState)
   async def get_onboarding_state(user_id: str):
       """
       Get onboarding state for user.
       
       Returns current progress, completed steps, and next step.
       """
       manager = get_onboarding_manager()
       state = manager.get_state(user_id)
       return state
   
   
   @router.post("/{user_id}/steps", response_model=OnboardingState)
   async def mark_step_complete(user_id: str, request: StepCompleteRequest):
       """
       Mark an onboarding step as complete.
       
       This is called automatically by the system when users complete actions.
       """
       manager = get_onboarding_manager()
       
       try:
           state = manager.mark_complete(user_id, request.step_id, request.interface)
           return state
       except Exception as e:
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=f"Failed to mark step complete: {str(e)}"
           )
   
   
   @router.get("/{user_id}/next", response_model=dict)
   async def get_next_step(user_id: str):
       """
       Get the next onboarding step for user.
       
       Returns step details and suggested actions.
       """
       manager = get_onboarding_manager()
       state = manager.get_state(user_id)
       next_step = state.get_next_step()
       
       if next_step is None:
           return {
               "completed": True,
               "message": "🎉 Onboarding complete! You're all set.",
           }
       
       # Add action suggestions
       actions = {
           "create_candidate": {
               "cli": "sono-eval candidate create --id your_id",
               "api": "POST /api/v1/candidates",
               "web": "Click 'New Candidate' button",
           },
           "first_assessment": {
               "cli": "sono-eval assess run --candidate-id your_id --file code.py",
               "api": "POST /api/v1/assessments",
               "web": "Upload code on Assessments page",
           },
           "view_results": {
               "cli": "sono-eval candidate history --id your_id",
               "api": "GET /api/v1/assessments/{id}",
               "web": "Click on any assessment",
           },
           "export_data": {
               "cli": "sono-eval assess run --output results.json",
               "api": "GET /api/v1/assessments/{id}/export",
               "web": "Click 'Export' button",
           },
           "try_another_interface": {
               "info": "Try CLI: pip install sono-eval",
               "web": "Explore API docs: /docs",
           },
       }
       
       return {
           "completed": False,
           "next_step": next_step.model_dump(),
           "progress": state.get_progress_percentage(),
           "actions": actions.get(next_step.step_id, {}),
       }
   ```

2. **Register Routes**
   ```python
   # src/sono_eval/api/main.py
   from sono_eval.api.routes import onboarding
   
   # Register onboarding routes
   app.include_router(onboarding.router)
   ```

3. **Auto-Track Onboarding Progress**
   - Modify assessment endpoint to mark "first_assessment" complete
   - Modify candidate creation to mark "create_candidate" complete
   
   ```python
   # In src/sono_eval/api/routes/assessments.py
   from sono_eval.onboarding import get_onboarding_manager
   
   @router.post("/", response_model=AssessmentResult)
   async def create_assessment(assessment_input: AssessmentInput):
       # ... existing code ...
       
       # Mark onboarding step complete
       manager = get_onboarding_manager()
       manager.mark_complete(
           assessment_input.candidate_id,
           "first_assessment",
           "api"
       )
       
       return result
   ```

**Validation:**
```bash
# Test API
curl http://localhost:8000/api/v1/onboarding/test_user

# Mark step complete
curl -X POST http://localhost:8000/api/v1/onboarding/test_user/steps \
  -H "Content-Type: application/json" \
  -d '{"step_id": "create_candidate", "interface": "api"}'

# Get next step
curl http://localhost:8000/api/v1/onboarding/test_user/next
```

---

## Phase 2: Web UI Welcome Tour (Priority: HIGHEST)

### Task 2.1: Implement Interactive Tour

**Objective:** Guide first-time Web UI users through core features

**Files to Create:**
- `frontend/components/Onboarding/WelcomeTour.tsx`
- `frontend/hooks/useOnboarding.ts`
- `frontend/lib/onboarding.ts`

**Dependencies to Add:**
```json
// frontend/package.json
{
  "dependencies": {
    "react-joyride": "^2.5.0"
  }
}
```

**Implementation:**

1. **Create Onboarding Hook**
   ```typescript
   // frontend/hooks/useOnboarding.ts
   import { useState, useEffect } from 'react';
   
   interface OnboardingState {
     user_id: string;
     completed: boolean;
     current_step: string | null;
     progress: number;
   }
   
   export function useOnboarding(userId: string) {
     const [state, setState] = useState<OnboardingState | null>(null);
     const [loading, setLoading] = useState(true);
     const [showTour, setShowTour] = useState(false);
     
     useEffect(() => {
       fetchOnboardingState();
     }, [userId]);
     
     const fetchOnboardingState = async () => {
       try {
         const response = await fetch(`/api/v1/onboarding/${userId}`);
         const data = await response.json();
         setState(data);
         
         // Show tour if not completed
         if (!data.completed && localStorage.getItem('tour_dismissed') !== 'true') {
           setShowTour(true);
         }
       } catch (error) {
         console.error('Failed to fetch onboarding state:', error);
       } finally {
         setLoading(false);
       }
     };
     
     const markStepComplete = async (stepId: string) => {
       try {
         await fetch(`/api/v1/onboarding/${userId}/steps`, {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ step_id: stepId, interface: 'web' }),
         });
         await fetchOnboardingState();
       } catch (error) {
         console.error('Failed to mark step complete:', error);
       }
     };
     
     const dismissTour = () => {
       setShowTour(false);
       localStorage.setItem('tour_dismissed', 'true');
     };
     
     const restartTour = () => {
       setShowTour(true);
       localStorage.removeItem('tour_dismissed');
     };
     
     return {
       state,
       loading,
       showTour,
       markStepComplete,
       dismissTour,
       restartTour,
     };
   }
   ```

2. **Create Welcome Tour Component**
   ```typescript
   // frontend/components/Onboarding/WelcomeTour.tsx
   import React from 'react';
   import Joyride, { Step, CallBackProps } from 'react-joyride';
   
   interface WelcomeTourProps {
     onComplete: () => void;
     onSkip: () => void;
   }
   
   export function WelcomeTour({ onComplete, onSkip }: WelcomeTourProps) {
     const steps: Step[] = [
       {
         target: 'body',
         content: (
           <div>
             <h2>Welcome to Sono-Eval! 👋</h2>
             <p>
               Let's take a quick tour to help you get started.
               This will only take 2 minutes.
             </p>
             <p>
               <small>You can skip this tour and access it later from Settings.</small>
             </p>
           </div>
         ),
         placement: 'center',
         disableBeacon: true,
       },
       {
         target: '[data-tour="create-candidate"]',
         content: (
           <div>
             <h3>Create Your Profile</h3>
             <p>
               Start by creating a candidate profile. This is where all your
               assessment history will be stored.
             </p>
           </div>
         ),
         placement: 'bottom',
       },
       {
         target: '[data-tour="run-assessment"]',
         content: (
           <div>
             <h3>Run Your First Assessment</h3>
             <p>
               Upload code or paste it directly. We'll evaluate it across
               multiple dimensions: Technical, Design, Collaboration, and more.
             </p>
           </div>
         ),
         placement: 'bottom',
       },
       {
         target: '[data-tour="view-results"]',
         content: (
           <div>
             <h3>View Detailed Results</h3>
             <p>
               See your scores, explanations, and actionable recommendations.
               Every score comes with evidence from your code.
             </p>
           </div>
         ),
         placement: 'bottom',
       },
       {
         target: '[data-tour="export-button"]',
         content: (
           <div>
             <h3>Export Your Data</h3>
             <p>
               Download your assessment results as JSON or PDF.
               Your data is yours to keep.
             </p>
           </div>
         ),
         placement: 'left',
       },
       {
         target: '[data-tour="api-docs"]',
         content: (
           <div>
             <h3>Explore Other Interfaces</h3>
             <p>
               Try our CLI for automation, API for integrations,
               or Mobile companion for guided assessments.
             </p>
           </div>
         ),
         placement: 'bottom',
       },
       {
         target: 'body',
         content: (
           <div>
             <h2>You're All Set! 🎉</h2>
             <p>
               Ready to run your first assessment? Click "New Assessment"
               to get started.
             </p>
             <p>
               <small>Need help? Check out the docs or ask in our community.</small>
             </p>
           </div>
         ),
         placement: 'center',
       },
     ];
     
     const handleJoyrideCallback = (data: CallBackProps) => {
       const { status, action } = data;
       
       if (status === 'finished' || status === 'skipped') {
         if (action === 'skip') {
           onSkip();
         } else {
           onComplete();
         }
       }
     };
     
     return (
       <Joyride
         steps={steps}
         continuous
         scrollToFirstStep
         showProgress
         showSkipButton
         callback={handleJoyrideCallback}
         styles={{
           options: {
             primaryColor: '#2196F3',
             zIndex: 10000,
           },
         }}
       />
     );
   }
   ```

3. **Integrate with Main Layout**
   ```typescript
   // frontend/app/layout.tsx
   'use client';
   
   import { useOnboarding } from '@/hooks/useOnboarding';
   import { WelcomeTour } from '@/components/Onboarding/WelcomeTour';
   
   export default function Layout({ children }: { children: React.ReactNode }) {
     const { showTour, dismissTour, markStepComplete } = useOnboarding('current_user');
     
     const handleTourComplete = () => {
       markStepComplete('viewed_tour');
       dismissTour();
     };
     
     return (
       <html>
         <body>
           {showTour && (
             <WelcomeTour
               onComplete={handleTourComplete}
               onSkip={dismissTour}
             />
           )}
           
           <nav>
             <button
               onClick={() => {
                 const { restartTour } = useOnboarding('current_user');
                 restartTour();
               }}
             >
               Show Tour Again
             </button>
           </nav>
           
           {children}
         </body>
       </html>
     );
   }
   ```

4. **Add Data Attributes to UI Elements**
   ```typescript
   // frontend/app/page.tsx
   <div>
     <button data-tour="create-candidate">New Candidate</button>
     <button data-tour="run-assessment">New Assessment</button>
     <div data-tour="view-results">
       {/* Assessment results */}
     </div>
     <button data-tour="export-button">Export</button>
     <a href="/docs" data-tour="api-docs">API Docs</a>
   </div>
   ```

**Validation:**
- Clear browser storage: `localStorage.clear()`
- Reload page: Should show tour automatically
- Complete tour: Should mark steps complete in backend
- Skip tour: Should not show again (unless "Show Tour Again" clicked)

---

## Phase 3: First Assessment Wizard (Priority: HIGH)

### Task 3.1: Create Guided Assessment Flow

**Objective:** Step-by-step wizard for first-time assessments

**Files to Create:**
- `frontend/components/Wizard/FirstAssessmentWizard.tsx`
- `frontend/components/Wizard/StepIndicator.tsx`

**Implementation:**

1. **Create Step Indicator**
   ```typescript
   // frontend/components/Wizard/StepIndicator.tsx
   import React from 'react';
   
   interface Step {
     id: string;
     name: string;
     completed: boolean;
   }
   
   interface StepIndicatorProps {
     steps: Step[];
     currentStep: number;
   }
   
   export function StepIndicator({ steps, currentStep }: StepIndicatorProps) {
     return (
       <div className="flex items-center justify-between w-full max-w-2xl mx-auto mb-8">
         {steps.map((step, index) => (
           <React.Fragment key={step.id}>
             <div className="flex flex-col items-center">
               <div
                 className={`
                   w-10 h-10 rounded-full flex items-center justify-center
                   ${index < currentStep ? 'bg-green-500 text-white' : ''}
                   ${index === currentStep ? 'bg-blue-500 text-white' : ''}
                   ${index > currentStep ? 'bg-gray-300 text-gray-600' : ''}
                 `}
               >
                 {index < currentStep ? '✓' : index + 1}
               </div>
               <div className="text-xs mt-2 text-center">{step.name}</div>
             </div>
             
             {index < steps.length - 1 && (
               <div
                 className={`
                   flex-1 h-1 mx-2
                   ${index < currentStep ? 'bg-green-500' : 'bg-gray-300'}
                 `}
               />
             )}
           </React.Fragment>
         ))}
       </div>
     );
   }
   ```

2. **Create Wizard Component**
   ```typescript
   // frontend/components/Wizard/FirstAssessmentWizard.tsx
   import React, { useState } from 'react';
   import { StepIndicator } from './StepIndicator';
   
   const SAMPLE_CODE = `def fibonacci(n):
       """Calculate fibonacci number."""
       if n <= 1:
           return n
       return fibonacci(n - 1) + fibonacci(n - 2)`;
   
   export function FirstAssessmentWizard({ onComplete }) {
     const [currentStep, setCurrentStep] = useState(0);
     const [formData, setFormData] = useState({
       candidateId: '',
       code: SAMPLE_CODE,
       paths: ['technical'],
     });
     
     const steps = [
       { id: 'select-path', name: 'Select Path', completed: false },
       { id: 'provide-code', name: 'Provide Code', completed: false },
       { id: 'run-assessment', name: 'Run Assessment', completed: false },
       { id: 'view-results', name: 'View Results', completed: false },
     ];
     
     const handleNext = () => {
       if (currentStep < steps.length - 1) {
         setCurrentStep(currentStep + 1);
       } else {
         onComplete();
       }
     };
     
     const handleBack = () => {
       if (currentStep > 0) {
         setCurrentStep(currentStep - 1);
       }
     };
     
     const renderStep = () => {
       switch (currentStep) {
         case 0:
           return (
             <div>
               <h2>Select Assessment Path</h2>
               <p>Choose which dimension to evaluate:</p>
               
               <div className="grid grid-cols-2 gap-4 mt-4">
                 {[
                   { id: 'technical', name: 'Technical', desc: 'Code quality, patterns' },
                   { id: 'design', name: 'Design', desc: 'Architecture, modularity' },
                   { id: 'collaboration', name: 'Collaboration', desc: 'Docs, readability' },
                   { id: 'problem_solving', name: 'Problem Solving', desc: 'Algorithms, logic' },
                 ].map(path => (
                   <button
                     key={path.id}
                     className={`
                       p-4 border rounded-lg text-left
                       ${formData.paths.includes(path.id) ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
                     `}
                     onClick={() => {
                       if (formData.paths.includes(path.id)) {
                         setFormData({
                           ...formData,
                           paths: formData.paths.filter(p => p !== path.id),
                         });
                       } else {
                         setFormData({
                           ...formData,
                           paths: [...formData.paths, path.id],
                         });
                       }
                     }}
                   >
                     <div className="font-bold">{path.name}</div>
                     <div className="text-sm text-gray-600">{path.desc}</div>
                   </button>
                 ))}
               </div>
               
               <p className="mt-4 text-sm text-gray-600">
                 💡 Tip: Start with "Technical" for your first assessment
               </p>
             </div>
           );
         
         case 1:
           return (
             <div>
               <h2>Provide Code</h2>
               <p>Paste your code or use our sample:</p>
               
               <textarea
                 className="w-full h-64 p-4 border rounded font-mono text-sm mt-4"
                 value={formData.code}
                 onChange={e => setFormData({ ...formData, code: e.target.value })}
                 placeholder="Paste your code here..."
               />
               
               <button
                 className="mt-2 text-blue-500"
                 onClick={() => setFormData({ ...formData, code: SAMPLE_CODE })}
               >
                 Use Sample Code
               </button>
               
               <p className="mt-4 text-sm text-gray-600">
                 💡 Tip: We support Python, JavaScript, Java, and more
               </p>
             </div>
           );
         
         case 2:
           return (
             <div>
               <h2>Run Assessment</h2>
               <p>Review your settings and run:</p>
               
               <div className="mt-4 p-4 bg-gray-50 rounded">
                 <div><strong>Paths:</strong> {formData.paths.join(', ')}</div>
                 <div className="mt-2"><strong>Code:</strong> {formData.code.split('\n').length} lines</div>
               </div>
               
               <button
                 className="mt-4 px-6 py-3 bg-blue-500 text-white rounded hover:bg-blue-600"
                 onClick={handleNext}
               >
                 Run Assessment →
               </button>
               
               <p className="mt-4 text-sm text-gray-600">
                 ⏱️ This usually takes 5-10 seconds
               </p>
             </div>
           );
         
         case 3:
           return (
             <div>
               <h2>View Results</h2>
               <p>Here's what we found:</p>
               
               {/* Show actual assessment results here */}
               
               <div className="mt-4 flex gap-4">
                 <button
                   className="px-6 py-3 bg-green-500 text-white rounded hover:bg-green-600"
                   onClick={onComplete}
                 >
                   Finish ✓
                 </button>
                 
                 <button
                   className="px-6 py-3 border rounded hover:bg-gray-50"
                   onClick={() => setCurrentStep(0)}
                 >
                   Run Another
                 </button>
               </div>
             </div>
           );
       }
     };
     
     return (
       <div className="max-w-4xl mx-auto p-8">
         <h1 className="text-3xl font-bold mb-8 text-center">
           First Assessment Wizard
         </h1>
         
         <StepIndicator steps={steps} currentStep={currentStep} />
         
         <div className="mt-8">
           {renderStep()}
         </div>
         
         <div className="mt-8 flex justify-between">
           {currentStep > 0 && currentStep < 3 && (
             <button
               className="px-4 py-2 border rounded hover:bg-gray-50"
               onClick={handleBack}
             >
               ← Back
             </button>
           )}
           
           {currentStep < 2 && (
             <button
               className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ml-auto"
               onClick={handleNext}
               disabled={formData.paths.length === 0}
             >
               Next →
             </button>
           )}
         </div>
       </div>
     );
   }
   ```

3. **Show Wizard for First-Time Users**
   ```typescript
   // frontend/app/assessments/new/page.tsx
   'use client';
   
   import { useOnboarding } from '@/hooks/useOnboarding';
   import { FirstAssessmentWizard } from '@/components/Wizard/FirstAssessmentWizard';
   
   export default function NewAssessmentPage() {
     const { state } = useOnboarding('current_user');
     
     const isFirstAssessment = state && !state.steps.find(
       s => s.step_id === 'first_assessment'
     )?.completed;
     
     if (isFirstAssessment) {
       return (
         <FirstAssessmentWizard
           onComplete={() => {
             // Redirect to results
             router.push('/assessments');
           }}
         />
       );
     }
     
     // Show regular assessment form
     return <AssessmentForm />;
   }
   ```

**Validation:**
- First-time user: Should see wizard
- Returning user: Should see regular form
- Complete wizard: Should mark "first_assessment" complete
- Wizard completion: Should be tracked in analytics

---

## Phase 4: Unified Terminology & Cross-Interface Discovery

### Task 4.1: Create Terminology Glossary

**Objective:** Consistent terms across all interfaces

**Files to Create:**
- `src/sono_eval/core/terminology.py`
- `Documentation/Guides/GLOSSARY.md`

**Implementation:**

1. **Define Terminology Map**
   ```python
   # src/sono_eval/core/terminology.py
   """Unified terminology across interfaces."""
   
   from typing import Dict
   
   TERMINOLOGY: Dict[str, Dict[str, str]] = {
       "candidate": {
           "name": "Candidate",
           "description": "A person being assessed",
           "cli_term": "candidate",
           "api_term": "candidate_id",
           "web_term": "Candidate",
           "mobile_term": "Your Profile",
           "aliases": ["user", "developer", "person"],
       },
       "assessment": {
           "name": "Assessment",
           "description": "Evaluation of code across multiple dimensions",
           "cli_term": "assessment",
           "api_term": "assessment",
           "web_term": "Assessment",
           "mobile_term": "Evaluation",
           "aliases": ["evaluation", "review", "analysis"],
       },
       "path": {
           "name": "Assessment Path",
           "description": "Dimension being evaluated (Technical, Design, etc.)",
           "cli_term": "path",
           "api_term": "paths_to_evaluate",
           "web_term": "Path",
           "mobile_term": "Focus Area",
           "aliases": ["dimension", "aspect", "category"],
       },
       "score": {
           "name": "Score",
           "description": "Numeric assessment result (0-100)",
           "cli_term": "score",
           "api_term": "overall_score",
           "web_term": "Score",
           "mobile_term": "Rating",
           "aliases": ["rating", "grade", "result"],
       },
   }
   
   
   def get_term_for_interface(term: str, interface: str) -> str:
       """Get interface-specific term."""
       if term not in TERMINOLOGY:
           return term
       
       term_info = TERMINOLOGY[term]
       return term_info.get(f"{interface}_term", term_info["name"])
   
   
   def get_term_description(term: str) -> str:
       """Get term description."""
       if term not in TERMINOLOGY:
           return ""
       
       return TERMINOLOGY[term]["description"]
   ```

2. **Add Tooltips to Web UI**
   ```typescript
   // frontend/components/Tooltip.tsx
   import { Tooltip as MuiTooltip } from '@mui/material';
   
   const TERMINOLOGY = {
     candidate: "A person being assessed",
     assessment: "Evaluation of code across multiple dimensions",
     path: "Dimension being evaluated (Technical, Design, etc.)",
     score: "Numeric assessment result (0-100)",
   };
   
   export function TermTooltip({ term, children }) {
     const description = TERMINOLOGY[term] || "";
     
     return (
       <MuiTooltip title={description} arrow>
         <span className="cursor-help underline decoration-dotted">
           {children}
         </span>
       </MuiTooltip>
     );
   }
   
   // Usage:
   // <TermTooltip term="candidate">Candidate</TermTooltip>
   ```

3. **Add to CLI Help**
   ```python
   # src/sono_eval/cli/commands/assess.py
   from sono_eval.core.terminology import get_term_description
   
   @click.option(
       '--paths',
       multiple=True,
       help=f"Assessment paths to evaluate. {get_term_description('path')}"
   )
   def assess_run(...):
       ...
   ```

---

### Task 4.2: Cross-Interface Discovery

**Objective:** Help users discover other interfaces

**Implementation:**

1. **Add Cross-Interface Links to Responses**
   ```python
   # src/sono_eval/api/main.py
   
   @app.post("/api/v1/assessments")
   async def create_assessment(...):
       result = await engine.assess(...)
       
       # Add cross-interface links to response
       response.headers["X-Web-UI-Link"] = f"http://localhost:3000/assessments/{result.assessment_id}"
       response.headers["X-CLI-Command"] = f"sono-eval candidate history --id {assessment_input.candidate_id}"
       
       return result
   ```

2. **Show Interface Suggestions in CLI**
   ```python
   # src/sono_eval/cli/commands/assess.py
   
   def display_results(result):
       """Display assessment results with cross-interface suggestions."""
       console = Console()
       
       # ... display results ...
       
       console.print("\n[bold]What's Next?[/bold]")
       console.print(f"  🌐 View in Web UI: http://localhost:3000/assessments/{result.assessment_id}")
       console.print(f"  📊 API endpoint: GET /api/v1/assessments/{result.assessment_id}")
       console.print(f"  📱 Mobile: Open Sono-Eval app and sync")
   ```

3. **Add "Try" Buttons to Web UI**
   ```typescript
   // frontend/components/InterfaceDiscovery.tsx
   
   export function InterfaceDiscovery() {
     return (
       <div className="border rounded p-4 bg-blue-50">
         <h3>Try Other Interfaces</h3>
         
         <div className="grid grid-cols-3 gap-4 mt-4">
           <div>
             <h4>CLI</h4>
             <p className="text-sm">Automate assessments</p>
             <code className="text-xs">pip install sono-eval</code>
           </div>
           
           <div>
             <h4>API</h4>
             <p className="text-sm">Integrate with your tools</p>
             <a href="/docs" className="text-blue-500">View Docs</a>
           </div>
           
           <div>
             <h4>Mobile</h4>
             <p className="text-sm">Guided assessments</p>
             <a href="/mobile" className="text-blue-500">Open Mobile</a>
           </div>
         </div>
       </div>
     );
   }
   ```

**Validation:**
- Run assessment via API: Check response headers for cross-interface links
- Run assessment via CLI: Verify Web UI link shown
- Check Web UI: Verify "Try Other Interfaces" section visible

---

## Testing & Validation

### End-to-End Test Scenarios

1. **First-Time User Flow (Web UI)**
   - User lands on homepage (no auth)
   - Welcome tour starts automatically
   - User creates candidate
   - User runs first assessment via wizard
   - User sees results with cross-interface suggestions
   - Success: All onboarding steps marked complete

2. **Cross-Interface Tracking**
   - User creates candidate via CLI
   - User runs assessment via API
   - User views results in Web UI
   - Verify: Onboarding state synced across interfaces

3. **Terminology Consistency**
   - Compare CLI help, API docs, Web UI labels
   - Verify: Same terms used everywhere
   - Test: Tooltips show correct descriptions

---

## Rollout Plan

### Pre-Launch
1. Implement onboarding framework
2. Add API endpoints
3. Build Web UI components
4. Add cross-interface links
5. Internal testing

### Launch (Staged)
1. Week 1: Onboarding framework (backend only)
2. Week 2: Web UI welcome tour
3. Week 3: First assessment wizard
4. Week 4: Cross-interface discovery

### Post-Launch
1. Monitor completion rates
2. Collect user feedback
3. A/B test tour variants
4. Iterate based on analytics

---

## Success Metrics

### Quantitative
- Web UI conversion: 80%+ complete first assessment
- Cross-interface adoption: 60%+ use 2+ interfaces
- Feature discovery: 70%+ use advanced features
- Time-to-value: 3-5 minutes

### Qualitative
- User feedback: 4.5/5 satisfaction
- Support questions: -40%
- "Confusing onboarding" feedback: -80%

---

## Related Documents
- [UX_ENHANCEMENT_ANALYSIS.md](UX_ENHANCEMENT_ANALYSIS.md) - Parent analysis
- [IMPLEMENTATION_GUIDE_AREA1_DOCUMENTATION.md](IMPLEMENTATION_GUIDE_AREA1_DOCUMENTATION.md) - Documentation guide
- [IMPLEMENTATION_GUIDE_AREA3_ERROR_RECOVERY.md](IMPLEMENTATION_GUIDE_AREA3_ERROR_RECOVERY.md) - Error recovery guide

---

**Version:** 1.0  
**Last Updated:** January 25, 2026  
**Status:** Ready for Implementation
