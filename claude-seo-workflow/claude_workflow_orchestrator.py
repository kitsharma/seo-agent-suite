"""
Claude SEO Workflow Orchestrator - Manages workflow execution and agent coordination

Path: /claude_workflow_orchestrator.py
Purpose: Orchestrates the execution of multiple specialized Claude SEO agents in 
         predefined sequences, creating complete workflows for different SEO tasks.
"""

import json
import time
import logging
from typing import Dict, List, Any

from claude_agent_framework import SEOWorkflow
from claude_seo_agents import (
    KeywordResearchAgent,
    ContentBriefAgent,
    ContentWriterAgent,
    TechnicalSEOAgent,
    ContentGapAnalysisAgent,
    SEOStrategyAgent
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/claude_seo_workflow.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ClaudeSEOWorkflowOrchestrator")


class ClaudeSEOWorkflowOrchestrator:
    """Orchestrates the end-to-end SEO workflow process using Claude agents"""
    
    def __init__(self, model=None):
        """Initialize the orchestrator with agents and workflow templates
        
        Args:
            model: Optional Claude model to use for all agents
        """
        # Initialize the main workflow
        self.workflow = SEOWorkflow()
        
        # Store the model selection
        self.model = model
        
        # Initialize all agents
        self.register_all_agents()
        
        # Define workflow templates
        self.workflow_templates = self._create_workflow_templates()
        
    def register_all_agents(self):
        """Register all SEO agents with the workflow"""
        logger.info("Registering Claude SEO agents...")
        
        self.workflow.register_agent("keyword_research", KeywordResearchAgent(self.model))
        self.workflow.register_agent("content_brief", ContentBriefAgent(self.model))
        self.workflow.register_agent("content_writer", ContentWriterAgent(self.model))
        self.workflow.register_agent("technical_seo", TechnicalSEOAgent(self.model))
        self.workflow.register_agent("content_gap_analysis", ContentGapAnalysisAgent(self.model))
        self.workflow.register_agent("seo_strategy", SEOStrategyAgent(self.model))
        
        logger.info("All agents registered successfully")
    
    def _create_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create predefined workflow templates for common SEO tasks"""
        return {
            "content_creation": {
                "steps": [
                    "keyword_research",
                    "content_brief",
                    "content_writer"
                ],
                "description": "Complete content creation workflow from keyword research to finished article"
            },
            "technical_audit": {
                "steps": [
                    "technical_seo"
                ],
                "description": "Technical SEO audit with prioritized recommendations"
            },
            "content_gap_analysis": {
                "steps": [
                    "keyword_research",
                    "content_gap_analysis"
                ],
                "description": "Identify content opportunities and gaps compared to competitors"
            },
            "comprehensive_seo": {
                "steps": [
                    "keyword_research",
                    "technical_seo",
                    "content_gap_analysis",
                    "seo_strategy"
                ],
                "description": "Complete SEO analysis and strategy development"
            }
        }
    
    def get_available_workflows(self) -> Dict[str, str]:
        """Get a list of available workflow templates with descriptions"""
        return {name: info["description"] for name, info in self.workflow_templates.items()}
    
    def run_workflow(self, workflow_type: str, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a predefined workflow template"""
        if workflow_type not in self.workflow_templates:
            available_workflows = list(self.workflow_templates.keys())
            raise ValueError(f"Unknown workflow type: {workflow_type}. Available workflows: {available_workflows}")
        
        workflow_info = self.workflow_templates[workflow_type]
        workflow_steps = workflow_info["steps"]
        
        logger.info(f"Starting workflow: {workflow_type} with {len(workflow_steps)} steps")
        
        start_time = time.time()
        result = self.workflow.execute_workflow(initial_data, workflow_steps)
        execution_time = time.time() - start_time
        
        logger.info(f"Workflow {workflow_type} completed in {execution_time:.2f} seconds")
        
        # Add execution summary to results
        result["execution_summary"] = self.workflow.get_execution_summary()
        result["workflow_type"] = workflow_type
        result["workflow_description"] = workflow_info["description"]
        
        return result
    
    def run_custom_workflow(self, steps: List[str], initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a custom workflow with specified steps"""
        # Validate that all steps have registered agents
        for step in steps:
            if step not in self.workflow.agents:
                available_agents = list(self.workflow.agents.keys())
                raise ValueError(f"No agent registered for step: {step}. Available agents: {available_agents}")
        
        logger.info(f"Starting custom workflow with {len(steps)} steps")
        
        start_time = time.time()
        result = self.workflow.execute_workflow(initial_data, steps)
        execution_time = time.time() - start_time
        
        logger.info(f"Custom workflow completed in {execution_time:.2f} seconds")
        
        # Add execution summary to results
        result["execution_summary"] = self.workflow.get_execution_summary()
        result["workflow_type"] = "custom"
        result["workflow_steps"] = steps
        
        return result
    
    def save_workflow_results(self, results: Dict[str, Any], filename: str) -> None:
        """Save workflow results to a file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Workflow results saved to {filename}")
        
    def get_agent_descriptions(self) -> Dict[str, str]:
        """Get descriptions of all available agents"""
        descriptions = {
            "keyword_research": "Discovers valuable keywords based on intent and business goals",
            "content_brief": "Creates comprehensive content briefs with strategic direction",
            "content_writer": "Generates naturally flowing, SEO-optimized content",
            "technical_seo": "Identifies technical SEO issues with prioritized recommendations",
            "content_gap_analysis": "Identifies content opportunities compared to competitors",
            "seo_strategy": "Develops comprehensive SEO strategies aligned with business goals"
        }
        
        return descriptions
