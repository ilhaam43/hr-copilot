from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json

class HRMetricsKPIData:
    """
    Kelas untuk menangani data metrics dan KPI HR yang komprehensif
    """
    
    def __init__(self):
        self.talent_acquisition_metrics = self._load_talent_acquisition_metrics()
        self.employee_engagement_metrics = self._load_employee_engagement_metrics()
        self.performance_metrics = self._load_performance_metrics()
        self.retention_turnover_metrics = self._load_retention_turnover_metrics()
        self.learning_development_metrics = self._load_learning_development_metrics()
        self.compensation_benefits_metrics = self._load_compensation_benefits_metrics()
        self.diversity_inclusion_metrics = self._load_diversity_inclusion_metrics()
        self.productivity_metrics = self._load_productivity_metrics()
        self.compliance_metrics = self._load_compliance_metrics()
        self.financial_metrics = self._load_financial_metrics()
        self.benchmarking_data = self._load_benchmarking_data()
        self.dashboard_templates = self._load_dashboard_templates()
    
    def _load_talent_acquisition_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk talent acquisition dan recruitment
        """
        return {
            'time_to_fill': {
                'definition': 'Average number of days from job posting to offer acceptance',
                'formula': 'Sum of (Offer Accept Date - Job Posted Date) / Number of Positions Filled',
                'unit': 'Days',
                'frequency': 'Monthly',
                'target_range': {
                    'excellent': '< 30 days',
                    'good': '30-45 days',
                    'average': '45-60 days',
                    'poor': '> 60 days'
                },
                'industry_benchmarks': {
                    'technology': 35,
                    'finance': 42,
                    'healthcare': 38,
                    'manufacturing': 45,
                    'retail': 28
                },
                'factors_affecting': [
                    'Job market conditions',
                    'Role complexity',
                    'Salary competitiveness',
                    'Hiring process efficiency',
                    'Employer brand strength'
                ],
                'improvement_strategies': [
                    'Streamline interview process',
                    'Improve job descriptions',
                    'Enhance employer branding',
                    'Use recruitment technology',
                    'Build talent pipelines'
                ]
            },
            'time_to_hire': {
                'definition': 'Average number of days from first candidate contact to offer acceptance',
                'formula': 'Sum of (Offer Accept Date - First Contact Date) / Number of Hires',
                'unit': 'Days',
                'frequency': 'Monthly',
                'target_range': {
                    'excellent': '< 20 days',
                    'good': '20-30 days',
                    'average': '30-40 days',
                    'poor': '> 40 days'
                },
                'industry_benchmarks': {
                    'technology': 25,
                    'finance': 32,
                    'healthcare': 28,
                    'manufacturing': 35,
                    'retail': 18
                }
            },
            'cost_per_hire': {
                'definition': 'Total recruitment costs divided by number of hires',
                'formula': '(Internal Costs + External Costs) / Number of Hires',
                'unit': 'Currency',
                'frequency': 'Quarterly',
                'components': {
                    'internal_costs': [
                        'Recruiter salaries',
                        'Hiring manager time',
                        'Interview time',
                        'Administrative costs'
                    ],
                    'external_costs': [
                        'Job board fees',
                        'Agency fees',
                        'Background checks',
                        'Assessment tools',
                        'Travel expenses'
                    ]
                },
                'industry_benchmarks': {
                    'technology': 15000,
                    'finance': 12000,
                    'healthcare': 8000,
                    'manufacturing': 6000,
                    'retail': 3000
                }
            },
            'quality_of_hire': {
                'definition': 'Measure of how well new hires perform and fit within the organization',
                'components': [
                    'Performance ratings',
                    'Retention rates',
                    'Time to productivity',
                    'Cultural fit scores',
                    'Manager satisfaction'
                ],
                'calculation_methods': [
                    'Weighted average of performance metrics',
                    'Retention rate at 12 months',
                    'Time to reach full productivity',
                    '360-degree feedback scores'
                ],
                'measurement_timeline': {
                    '90_days': 'Initial performance assessment',
                    '6_months': 'Mid-term evaluation',
                    '12_months': 'Annual quality assessment'
                }
            },
            'source_effectiveness': {
                'definition': 'Performance of different recruitment sources',
                'metrics': [
                    'Applications per source',
                    'Interview rate by source',
                    'Hire rate by source',
                    'Quality of hire by source',
                    'Cost per hire by source'
                ],
                'common_sources': [
                    'Company website',
                    'Job boards',
                    'Social media',
                    'Employee referrals',
                    'Recruitment agencies',
                    'University partnerships',
                    'Professional networks'
                ]
            },
            'candidate_experience': {
                'definition': 'Measure of candidate satisfaction with recruitment process',
                'measurement_methods': [
                    'Post-interview surveys',
                    'Application completion rates',
                    'Offer acceptance rates',
                    'Glassdoor ratings',
                    'Net Promoter Score (NPS)'
                ],
                'key_touchpoints': [
                    'Job application process',
                    'Initial screening',
                    'Interview experience',
                    'Communication quality',
                    'Offer process',
                    'Onboarding transition'
                ]
            },
            'diversity_hiring': {
                'definition': 'Metrics tracking diversity in hiring process',
                'metrics': [
                    'Diversity of applicant pool',
                    'Interview-to-hire ratios by demographic',
                    'Offer acceptance rates by demographic',
                    'Time to hire by demographic',
                    'Source effectiveness for diverse candidates'
                ],
                'reporting_dimensions': [
                    'Gender',
                    'Ethnicity',
                    'Age groups',
                    'Educational background',
                    'Geographic location'
                ]
            }
        }
    
    def _load_employee_engagement_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk employee engagement
        """
        return {
            'engagement_score': {
                'definition': 'Overall measure of employee emotional commitment and involvement',
                'measurement_methods': [
                    'Annual engagement surveys',
                    'Pulse surveys',
                    'Stay interviews',
                    'Focus groups',
                    'Behavioral indicators'
                ],
                'key_dimensions': [
                    'Emotional engagement',
                    'Cognitive engagement',
                    'Physical engagement',
                    'Job satisfaction',
                    'Organizational commitment'
                ],
                'scoring_scale': {
                    'highly_engaged': '4.5-5.0',
                    'engaged': '3.5-4.4',
                    'neutral': '2.5-3.4',
                    'disengaged': '1.5-2.4',
                    'highly_disengaged': '1.0-1.4'
                },
                'industry_benchmarks': {
                    'technology': 4.1,
                    'finance': 3.8,
                    'healthcare': 3.9,
                    'manufacturing': 3.6,
                    'retail': 3.4
                }
            },
            'employee_net_promoter_score': {
                'definition': 'Likelihood of employees to recommend company as place to work',
                'calculation': 'Percentage of Promoters - Percentage of Detractors',
                'scale': {
                    'promoters': '9-10 (Highly likely to recommend)',
                    'passives': '7-8 (Neutral)',
                    'detractors': '0-6 (Unlikely to recommend)'
                },
                'benchmarks': {
                    'world_class': '> 50',
                    'excellent': '30-50',
                    'good': '10-30',
                    'poor': '< 10'
                }
            },
            'pulse_survey_participation': {
                'definition': 'Percentage of employees participating in pulse surveys',
                'formula': '(Number of Survey Responses / Total Employees) * 100',
                'target_rates': {
                    'excellent': '> 85%',
                    'good': '70-85%',
                    'average': '50-70%',
                    'poor': '< 50%'
                },
                'factors_affecting': [
                    'Survey frequency',
                    'Survey length',
                    'Communication quality',
                    'Action on feedback',
                    'Anonymity assurance'
                ]
            },
            'recognition_frequency': {
                'definition': 'How often employees receive recognition',
                'measurement_methods': [
                    'Recognition platform data',
                    'Manager feedback frequency',
                    'Peer recognition instances',
                    'Formal award programs'
                ],
                'target_frequency': {
                    'optimal': 'Weekly recognition',
                    'good': 'Bi-weekly recognition',
                    'minimum': 'Monthly recognition'
                }
            },
            'work_life_balance_score': {
                'definition': 'Employee perception of work-life balance',
                'measurement_areas': [
                    'Workload management',
                    'Flexible work options',
                    'Time off utilization',
                    'After-hours communication',
                    'Stress levels'
                ],
                'improvement_indicators': [
                    'Flexible work adoption rates',
                    'Vacation utilization rates',
                    'Overtime frequency',
                    'Burnout indicators'
                ]
            },
            'manager_effectiveness': {
                'definition': 'Quality of management as perceived by employees',
                'key_areas': [
                    'Communication skills',
                    'Support and development',
                    'Recognition and feedback',
                    'Decision making',
                    'Team building'
                ],
                'measurement_methods': [
                    'Upward feedback surveys',
                    '360-degree reviews',
                    'Skip-level meetings',
                    'Team engagement scores'
                ]
            }
        }
    
    def _load_performance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk performance management
        """
        return {
            'performance_rating_distribution': {
                'definition': 'Distribution of performance ratings across organization',
                'typical_distribution': {
                    'exceeds_expectations': '10-15%',
                    'meets_expectations': '70-80%',
                    'below_expectations': '5-10%',
                    'unsatisfactory': '< 5%'
                },
                'analysis_points': [
                    'Rating inflation trends',
                    'Manager calibration',
                    'Department variations',
                    'Correlation with business results'
                ]
            },
            'goal_completion_rate': {
                'definition': 'Percentage of employee goals completed on time',
                'formula': '(Goals Completed / Total Goals Set) * 100',
                'target_rates': {
                    'excellent': '> 90%',
                    'good': '80-90%',
                    'average': '70-80%',
                    'poor': '< 70%'
                },
                'factors_for_success': [
                    'SMART goal setting',
                    'Regular check-ins',
                    'Resource availability',
                    'Clear priorities',
                    'Manager support'
                ]
            },
            'feedback_frequency': {
                'definition': 'How often employees receive performance feedback',
                'measurement': [
                    'Formal review frequency',
                    'Informal feedback instances',
                    'Peer feedback frequency',
                    'Real-time feedback tools usage'
                ],
                'best_practices': {
                    'continuous_feedback': 'Weekly or bi-weekly',
                    'formal_reviews': 'Quarterly or bi-annually',
                    'peer_feedback': 'Monthly or quarterly'
                }
            },
            'development_plan_completion': {
                'definition': 'Percentage of employees with completed development plans',
                'components': [
                    'Skills gap analysis',
                    'Learning objectives',
                    'Development activities',
                    'Timeline and milestones',
                    'Progress tracking'
                ],
                'success_metrics': [
                    'Plan creation rate',
                    'Activity completion rate',
                    'Skill improvement measurement',
                    'Career progression correlation'
                ]
            },
            'performance_improvement_success': {
                'definition': 'Success rate of performance improvement plans',
                'measurement': [
                    'PIP completion rates',
                    'Performance improvement achieved',
                    'Retention after PIP',
                    'Time to improvement'
                ],
                'success_factors': [
                    'Clear expectations',
                    'Regular monitoring',
                    'Adequate support',
                    'Realistic timelines'
                ]
            },
            'high_performer_retention': {
                'definition': 'Retention rate of top performing employees',
                'calculation': '(High Performers Retained / Total High Performers) * 100',
                'target_rate': '> 95%',
                'retention_strategies': [
                    'Career development opportunities',
                    'Competitive compensation',
                    'Recognition programs',
                    'Challenging assignments',
                    'Leadership development'
                ]
            }
        }
    
    def _load_retention_turnover_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk retention dan turnover
        """
        return {
            'overall_turnover_rate': {
                'definition': 'Percentage of employees who leave organization in given period',
                'formula': '(Number of Separations / Average Number of Employees) * 100',
                'calculation_periods': [
                    'Monthly turnover',
                    'Quarterly turnover',
                    'Annual turnover'
                ],
                'industry_benchmarks': {
                    'technology': 13.2,
                    'finance': 10.8,
                    'healthcare': 15.1,
                    'manufacturing': 12.3,
                    'retail': 22.5
                },
                'target_ranges': {
                    'excellent': '< 10%',
                    'good': '10-15%',
                    'average': '15-20%',
                    'concerning': '> 20%'
                }
            },
            'voluntary_vs_involuntary': {
                'definition': 'Breakdown of turnover by voluntary and involuntary separations',
                'voluntary_reasons': [
                    'Better opportunity',
                    'Career advancement',
                    'Compensation',
                    'Work-life balance',
                    'Management issues',
                    'Company culture',
                    'Relocation'
                ],
                'involuntary_reasons': [
                    'Performance issues',
                    'Policy violations',
                    'Restructuring',
                    'Budget cuts',
                    'Position elimination'
                ]
            },
            'regrettable_vs_non_regrettable': {
                'definition': 'Classification of turnover based on impact to organization',
                'regrettable_turnover': {
                    'definition': 'Loss of employees organization wanted to retain',
                    'characteristics': [
                        'High performers',
                        'Critical skills',
                        'Hard to replace',
                        'High potential',
                        'Cultural contributors'
                    ]
                },
                'non_regrettable_turnover': {
                    'definition': 'Loss of employees organization did not want to retain',
                    'characteristics': [
                        'Poor performers',
                        'Cultural misfits',
                        'Disciplinary issues',
                        'Redundant skills'
                    ]
                }
            },
            'turnover_by_tenure': {
                'definition': 'Turnover rates segmented by length of service',
                'tenure_segments': {
                    '0-6_months': 'New hire turnover',
                    '6-12_months': 'Early career turnover',
                    '1-2_years': 'Early tenure turnover',
                    '2-5_years': 'Mid-tenure turnover',
                    '5+_years': 'Veteran turnover'
                },
                'analysis_insights': [
                    'Onboarding effectiveness',
                    'Role clarity issues',
                    'Career development gaps',
                    'Compensation competitiveness'
                ]
            },
            'retention_rate_by_segment': {
                'definition': 'Retention rates for different employee segments',
                'segments': [
                    'Department/Function',
                    'Job level',
                    'Performance rating',
                    'Age groups',
                    'Gender',
                    'Location',
                    'Manager'
                ],
                'analysis_value': [
                    'Identify at-risk groups',
                    'Target retention efforts',
                    'Address systemic issues',
                    'Measure program effectiveness'
                ]
            },
            'cost_of_turnover': {
                'definition': 'Total cost associated with employee turnover',
                'cost_components': {
                    'separation_costs': [
                        'Exit interviews',
                        'Administrative processing',
                        'Severance payments',
                        'Unused vacation payout'
                    ],
                    'replacement_costs': [
                        'Recruitment expenses',
                        'Interview time',
                        'Background checks',
                        'Relocation expenses'
                    ],
                    'training_costs': [
                        'Orientation programs',
                        'Formal training',
                        'On-the-job training',
                        'Mentoring time'
                    ],
                    'productivity_loss': [
                        'Learning curve impact',
                        'Reduced team productivity',
                        'Customer relationship impact',
                        'Knowledge loss'
                    ]
                },
                'calculation_methods': [
                    'Direct cost calculation',
                    'Percentage of annual salary',
                    'Industry benchmarking'
                ]
            }
        }
    
    def _load_learning_development_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk learning dan development
        """
        return {
            'training_completion_rate': {
                'definition': 'Percentage of assigned training completed by employees',
                'formula': '(Completed Training Sessions / Assigned Training Sessions) * 100',
                'target_rates': {
                    'excellent': '> 95%',
                    'good': '85-95%',
                    'average': '75-85%',
                    'poor': '< 75%'
                },
                'factors_affecting': [
                    'Training relevance',
                    'Time allocation',
                    'Manager support',
                    'Training quality',
                    'Delivery method'
                ]
            },
            'learning_hours_per_employee': {
                'definition': 'Average number of learning hours per employee annually',
                'industry_benchmarks': {
                    'technology': 40,
                    'finance': 35,
                    'healthcare': 45,
                    'manufacturing': 30,
                    'retail': 25
                },
                'breakdown_by_type': [
                    'Formal classroom training',
                    'Online learning',
                    'On-the-job training',
                    'Conferences and seminars',
                    'Mentoring and coaching'
                ]
            },
            'skill_development_progress': {
                'definition': 'Measurement of skill improvement over time',
                'measurement_methods': [
                    'Pre and post assessments',
                    'Skill gap analysis',
                    'Performance improvements',
                    'Certification achievements',
                    'Manager evaluations'
                ],
                'tracking_dimensions': [
                    'Technical skills',
                    'Soft skills',
                    'Leadership skills',
                    'Industry-specific skills'
                ]
            },
            'training_effectiveness': {
                'definition': 'Measure of training impact on performance and behavior',
                'kirkpatrick_levels': {
                    'level_1_reaction': 'Participant satisfaction with training',
                    'level_2_learning': 'Knowledge and skill acquisition',
                    'level_3_behavior': 'Application of learning on the job',
                    'level_4_results': 'Business impact and ROI'
                },
                'measurement_timeline': {
                    'immediate': 'Post-training surveys',
                    '30_days': 'Knowledge retention tests',
                    '90_days': 'Behavior change assessment',
                    '6_months': 'Performance impact analysis'
                }
            },
            'internal_mobility_rate': {
                'definition': 'Percentage of positions filled by internal candidates',
                'formula': '(Internal Hires / Total Hires) * 100',
                'target_rates': {
                    'excellent': '> 70%',
                    'good': '50-70%',
                    'average': '30-50%',
                    'poor': '< 30%'
                },
                'benefits': [
                    'Reduced hiring costs',
                    'Faster time to productivity',
                    'Improved retention',
                    'Enhanced employee engagement'
                ]
            },
            'leadership_development_pipeline': {
                'definition': 'Strength of leadership development programs',
                'metrics': [
                    'High-potential identification rate',
                    'Leadership program completion',
                    'Promotion rate from programs',
                    'Leadership readiness scores',
                    'Succession planning coverage'
                ],
                'pipeline_health_indicators': [
                    'Bench strength by level',
                    'Ready-now candidates',
                    'Development program effectiveness',
                    'Leadership retention rates'
                ]
            }
        }
    
    def _load_compensation_benefits_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk compensation dan benefits
        """
        return {
            'compensation_ratio': {
                'definition': 'Employee salary compared to market median',
                'formula': 'Employee Salary / Market Median Salary',
                'interpretation': {
                    '> 1.15': 'Above market (potential overpay)',
                    '0.95-1.15': 'Market competitive',
                    '0.85-0.95': 'Below market (retention risk)',
                    '< 0.85': 'Significantly below market'
                },
                'analysis_dimensions': [
                    'By job level',
                    'By department',
                    'By performance rating',
                    'By tenure',
                    'By location'
                ]
            },
            'pay_equity_analysis': {
                'definition': 'Analysis of pay differences across demographic groups',
                'key_metrics': [
                    'Gender pay gap',
                    'Ethnicity pay gap',
                    'Age-based pay differences',
                    'Pay range penetration'
                ],
                'analysis_methods': [
                    'Statistical regression analysis',
                    'Cohort comparisons',
                    'Job-level analysis',
                    'Adjusted pay gap calculations'
                ],
                'remediation_tracking': [
                    'Pay adjustment amounts',
                    'Timeline for corrections',
                    'Progress monitoring',
                    'Ongoing compliance'
                ]
            },
            'benefits_utilization': {
                'definition': 'Employee usage of available benefits programs',
                'key_benefits': {
                    'health_insurance': {
                        'participation_rate': 'Percentage enrolled',
                        'cost_per_employee': 'Average annual cost',
                        'satisfaction_score': 'Employee satisfaction rating'
                    },
                    'retirement_plans': {
                        'participation_rate': 'Percentage contributing',
                        'average_contribution': 'Average contribution percentage',
                        'employer_match_utilization': 'Percentage maximizing match'
                    },
                    'flexible_work': {
                        'remote_work_adoption': 'Percentage using remote work',
                        'flexible_hours_usage': 'Percentage using flexible schedules',
                        'satisfaction_scores': 'Employee satisfaction with flexibility'
                    }
                }
            },
            'total_rewards_perception': {
                'definition': 'Employee understanding and appreciation of total compensation',
                'components': [
                    'Base salary awareness',
                    'Benefits value understanding',
                    'Incentive program clarity',
                    'Career development value',
                    'Work-life balance appreciation'
                ],
                'measurement_methods': [
                    'Total rewards statements',
                    'Employee surveys',
                    'Focus groups',
                    'Benefits fairs feedback'
                ]
            },
            'compensation_budget_variance': {
                'definition': 'Actual compensation costs vs budgeted amounts',
                'variance_categories': [
                    'Salary increases',
                    'Bonus payments',
                    'Benefits costs',
                    'New hire premiums',
                    'Retention adjustments'
                ],
                'analysis_frequency': 'Monthly and quarterly reviews'
            }
        }
    
    def _load_diversity_inclusion_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk diversity dan inclusion
        """
        return {
            'workforce_diversity': {
                'definition': 'Representation of different demographic groups',
                'measurement_dimensions': [
                    'Gender representation',
                    'Ethnic/racial diversity',
                    'Age distribution',
                    'Educational background',
                    'Geographic diversity',
                    'Disability status',
                    'Veteran status'
                ],
                'analysis_levels': [
                    'Overall workforce',
                    'Leadership levels',
                    'Department/function',
                    'Job families',
                    'Geographic locations'
                ]
            },
            'inclusion_index': {
                'definition': 'Measure of how included employees feel in the workplace',
                'key_components': [
                    'Sense of belonging',
                    'Voice and input opportunities',
                    'Fair treatment perception',
                    'Career advancement equity',
                    'Cultural acceptance'
                ],
                'measurement_methods': [
                    'Inclusion surveys',
                    'Focus groups',
                    'Stay interviews',
                    'Exit interview analysis'
                ]
            },
            'leadership_diversity': {
                'definition': 'Diversity representation in leadership positions',
                'measurement_levels': [
                    'Executive team',
                    'Senior management',
                    'Middle management',
                    'First-line supervisors'
                ],
                'progression_tracking': [
                    'Promotion rates by demographic',
                    'Leadership pipeline diversity',
                    'Succession planning diversity',
                    'High-potential program participation'
                ]
            },
            'pay_equity_by_demographics': {
                'definition': 'Compensation equity across demographic groups',
                'analysis_methods': [
                    'Statistical pay gap analysis',
                    'Job-level comparisons',
                    'Performance-adjusted analysis',
                    'Tenure-adjusted comparisons'
                ],
                'reporting_requirements': [
                    'Annual pay equity reports',
                    'Regulatory compliance',
                    'Board reporting',
                    'Public disclosure'
                ]
            },
            'diverse_hiring_metrics': {
                'definition': 'Diversity in recruitment and hiring processes',
                'pipeline_metrics': [
                    'Diverse candidate sourcing',
                    'Application rates by demographic',
                    'Interview rates by demographic',
                    'Offer rates by demographic',
                    'Acceptance rates by demographic'
                ],
                'process_metrics': [
                    'Diverse interview panel usage',
                    'Bias training completion',
                    'Structured interview adoption',
                    'Diverse recruiter assignments'
                ]
            }
        }
    
    def _load_productivity_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk produktivitas karyawan
        """
        return {
            'revenue_per_employee': {
                'definition': 'Total revenue divided by number of employees',
                'formula': 'Total Revenue / Average Number of Employees',
                'industry_benchmarks': {
                    'technology': 400000,
                    'finance': 350000,
                    'healthcare': 200000,
                    'manufacturing': 250000,
                    'retail': 150000
                },
                'factors_affecting': [
                    'Business model',
                    'Automation level',
                    'Employee skills',
                    'Technology adoption',
                    'Process efficiency'
                ]
            },
            'profit_per_employee': {
                'definition': 'Net profit divided by number of employees',
                'formula': 'Net Profit / Average Number of Employees',
                'analysis_considerations': [
                    'Industry variations',
                    'Business cycle impacts',
                    'Investment phases',
                    'Market conditions'
                ]
            },
            'absenteeism_rate': {
                'definition': 'Percentage of scheduled work time lost due to absences',
                'formula': '(Total Absence Hours / Total Scheduled Hours) * 100',
                'target_rates': {
                    'excellent': '< 2%',
                    'good': '2-3%',
                    'average': '3-5%',
                    'concerning': '> 5%'
                },
                'absence_categories': [
                    'Planned absences (vacation, personal)',
                    'Unplanned absences (sick, emergency)',
                    'FMLA/medical leave',
                    'Other approved leave'
                ]
            },
            'overtime_utilization': {
                'definition': 'Amount and cost of overtime work',
                'metrics': [
                    'Overtime hours percentage',
                    'Overtime cost as % of payroll',
                    'Employees working overtime',
                    'Average overtime per employee'
                ],
                'analysis_points': [
                    'Staffing adequacy',
                    'Workload distribution',
                    'Seasonal patterns',
                    'Cost efficiency'
                ]
            },
            'employee_utilization_rate': {
                'definition': 'Percentage of employee time spent on productive activities',
                'calculation_methods': [
                    'Billable hours tracking',
                    'Project time allocation',
                    'Activity-based measurement',
                    'Output-based assessment'
                ],
                'improvement_strategies': [
                    'Process optimization',
                    'Technology adoption',
                    'Skills development',
                    'Workload balancing'
                ]
            }
        }
    
    def _load_compliance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics untuk compliance dan regulatory
        """
        return {
            'training_compliance_rate': {
                'definition': 'Percentage of required compliance training completed',
                'formula': '(Completed Required Training / Total Required Training) * 100',
                'target_rate': '100%',
                'tracking_categories': [
                    'Safety training',
                    'Anti-harassment training',
                    'Data privacy training',
                    'Ethics training',
                    'Industry-specific compliance'
                ]
            },
            'policy_acknowledgment_rate': {
                'definition': 'Percentage of employees who have acknowledged policies',
                'key_policies': [
                    'Code of conduct',
                    'Anti-harassment policy',
                    'Data privacy policy',
                    'Safety policies',
                    'Conflict of interest policy'
                ],
                'tracking_requirements': [
                    'Initial acknowledgment',
                    'Annual re-acknowledgment',
                    'Policy update acknowledgment'
                ]
            },
            'audit_findings': {
                'definition': 'Number and severity of compliance audit findings',
                'severity_levels': [
                    'Critical findings',
                    'High-risk findings',
                    'Medium-risk findings',
                    'Low-risk findings'
                ],
                'remediation_tracking': [
                    'Finding resolution time',
                    'Corrective action completion',
                    'Follow-up audit results'
                ]
            },
            'incident_reporting': {
                'definition': 'Tracking of workplace incidents and violations',
                'incident_types': [
                    'Safety incidents',
                    'Harassment complaints',
                    'Ethics violations',
                    'Policy breaches',
                    'Discrimination claims'
                ],
                'metrics': [
                    'Incident frequency',
                    'Resolution time',
                    'Repeat incidents',
                    'Preventive actions taken'
                ]
            }
        }
    
    def _load_financial_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Metrics finansial HR
        """
        return {
            'hr_cost_per_employee': {
                'definition': 'Total HR department costs divided by number of employees',
                'formula': 'Total HR Costs / Total Number of Employees',
                'cost_components': [
                    'HR staff salaries and benefits',
                    'HR technology costs',
                    'Training and development',
                    'Recruitment expenses',
                    'External consulting fees'
                ],
                'industry_benchmarks': {
                    'technology': 2500,
                    'finance': 3000,
                    'healthcare': 2800,
                    'manufacturing': 2200,
                    'retail': 1800
                }
            },
            'hr_roi_metrics': {
                'definition': 'Return on investment for HR programs and initiatives',
                'calculation_areas': [
                    'Training program ROI',
                    'Retention program ROI',
                    'Recruitment process ROI',
                    'Employee engagement ROI',
                    'Technology implementation ROI'
                ],
                'roi_calculation': '(Benefits - Costs) / Costs * 100'
            },
            'benefits_cost_per_employee': {
                'definition': 'Total benefits costs divided by number of employees',
                'cost_breakdown': [
                    'Health insurance premiums',
                    'Retirement plan contributions',
                    'Paid time off costs',
                    'Other insurance premiums',
                    'Wellness program costs'
                ],
                'benchmarking': [
                    'Industry comparisons',
                    'Geographic variations',
                    'Company size adjustments'
                ]
            }
        }
    
    def _load_benchmarking_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Data benchmarking industri
        """
        return {
            'industry_benchmarks': {
                'technology': {
                    'turnover_rate': 13.2,
                    'time_to_fill': 35,
                    'cost_per_hire': 15000,
                    'engagement_score': 4.1,
                    'training_hours': 40,
                    'revenue_per_employee': 400000
                },
                'finance': {
                    'turnover_rate': 10.8,
                    'time_to_fill': 42,
                    'cost_per_hire': 12000,
                    'engagement_score': 3.8,
                    'training_hours': 35,
                    'revenue_per_employee': 350000
                },
                'healthcare': {
                    'turnover_rate': 15.1,
                    'time_to_fill': 38,
                    'cost_per_hire': 8000,
                    'engagement_score': 3.9,
                    'training_hours': 45,
                    'revenue_per_employee': 200000
                },
                'manufacturing': {
                    'turnover_rate': 12.3,
                    'time_to_fill': 45,
                    'cost_per_hire': 6000,
                    'engagement_score': 3.6,
                    'training_hours': 30,
                    'revenue_per_employee': 250000
                },
                'retail': {
                    'turnover_rate': 22.5,
                    'time_to_fill': 28,
                    'cost_per_hire': 3000,
                    'engagement_score': 3.4,
                    'training_hours': 25,
                    'revenue_per_employee': 150000
                }
            },
            'company_size_benchmarks': {
                'small_company': {
                    'employee_range': '< 100',
                    'hr_staff_ratio': '1:25',
                    'hr_cost_per_employee': 1500,
                    'technology_adoption': 'Basic HRIS'
                },
                'medium_company': {
                    'employee_range': '100-1000',
                    'hr_staff_ratio': '1:50',
                    'hr_cost_per_employee': 2000,
                    'technology_adoption': 'Integrated HR suite'
                },
                'large_company': {
                    'employee_range': '1000-10000',
                    'hr_staff_ratio': '1:75',
                    'hr_cost_per_employee': 2500,
                    'technology_adoption': 'Enterprise HR platform'
                },
                'enterprise': {
                    'employee_range': '> 10000',
                    'hr_staff_ratio': '1:100',
                    'hr_cost_per_employee': 3000,
                    'technology_adoption': 'Advanced analytics & AI'
                }
            }
        }
    
    def _load_dashboard_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Template dashboard untuk berbagai stakeholder
        """
        return {
            'executive_dashboard': {
                'target_audience': 'C-level executives and board members',
                'key_metrics': [
                    'Overall turnover rate',
                    'Employee engagement score',
                    'Revenue per employee',
                    'HR cost per employee',
                    'Diversity metrics',
                    'Talent pipeline strength'
                ],
                'visualization_types': [
                    'KPI scorecards',
                    'Trend charts',
                    'Benchmark comparisons',
                    'Heat maps'
                ],
                'update_frequency': 'Monthly'
            },
            'hr_leadership_dashboard': {
                'target_audience': 'HR directors and managers',
                'key_metrics': [
                    'Recruitment metrics',
                    'Performance management',
                    'Learning and development',
                    'Employee relations',
                    'Compliance status',
                    'Budget utilization'
                ],
                'visualization_types': [
                    'Detailed scorecards',
                    'Drill-down capabilities',
                    'Comparative analysis',
                    'Action item tracking'
                ],
                'update_frequency': 'Weekly'
            },
            'manager_dashboard': {
                'target_audience': 'People managers and supervisors',
                'key_metrics': [
                    'Team engagement scores',
                    'Performance ratings',
                    'Turnover risk indicators',
                    'Training completion',
                    'Goal achievement',
                    'Team diversity'
                ],
                'visualization_types': [
                    'Team scorecards',
                    'Individual employee cards',
                    'Alert notifications',
                    'Action recommendations'
                ],
                'update_frequency': 'Real-time'
            },
            'employee_dashboard': {
                'target_audience': 'Individual employees',
                'key_metrics': [
                    'Personal performance',
                    'Goal progress',
                    'Learning achievements',
                    'Career development',
                    'Benefits utilization',
                    'Recognition received'
                ],
                'visualization_types': [
                    'Personal scorecards',
                    'Progress tracking',
                    'Recommendation engines',
                    'Peer comparisons'
                ],
                'update_frequency': 'Real-time'
            }
        }
    
    def get_metric_info(self, category: str, metric: str = None) -> Dict[str, Any]:
        """
        Mendapatkan informasi metric tertentu
        """
        category_map = {
            'talent_acquisition': self.talent_acquisition_metrics,
            'employee_engagement': self.employee_engagement_metrics,
            'performance': self.performance_metrics,
            'retention_turnover': self.retention_turnover_metrics,
            'learning_development': self.learning_development_metrics,
            'compensation_benefits': self.compensation_benefits_metrics,
            'diversity_inclusion': self.diversity_inclusion_metrics,
            'productivity': self.productivity_metrics,
            'compliance': self.compliance_metrics,
            'financial': self.financial_metrics
        }
        
        if category in category_map:
            if metric:
                return category_map[category].get(metric, {})
            return category_map[category]
        return {}
    
    def get_benchmark_data(self, industry: str = None, company_size: str = None) -> Dict[str, Any]:
        """
        Mendapatkan data benchmark
        """
        result = {}
        
        if industry and industry in self.benchmarking_data['industry_benchmarks']:
            result['industry'] = self.benchmarking_data['industry_benchmarks'][industry]
        
        if company_size and company_size in self.benchmarking_data['company_size_benchmarks']:
            result['company_size'] = self.benchmarking_data['company_size_benchmarks'][company_size]
        
        if not result:
            result = self.benchmarking_data
        
        return result
    
    def get_dashboard_template(self, dashboard_type: str) -> Dict[str, Any]:
        """
        Mendapatkan template dashboard
        """
        return self.dashboard_templates.get(dashboard_type, {})
    
    def search_metrics(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """
        Mencari metrics berdasarkan query
        """
        results = []
        query_lower = query.lower()
        
        # Define all metric categories
        all_categories = {
            'talent_acquisition': self.talent_acquisition_metrics,
            'employee_engagement': self.employee_engagement_metrics,
            'performance': self.performance_metrics,
            'retention_turnover': self.retention_turnover_metrics,
            'learning_development': self.learning_development_metrics,
            'compensation_benefits': self.compensation_benefits_metrics,
            'diversity_inclusion': self.diversity_inclusion_metrics,
            'productivity': self.productivity_metrics,
            'compliance': self.compliance_metrics,
            'financial': self.financial_metrics
        }
        
        # Search through categories
        for cat_name, cat_data in all_categories.items():
            if category and cat_name != category:
                continue
            
            for metric_name, metric_data in cat_data.items():
                # Check if query matches metric name or definition
                if (query_lower in metric_name.lower() or 
                    query_lower in metric_data.get('definition', '').lower()):
                    
                    results.append({
                        'category': cat_name,
                        'metric': metric_name,
                        'data': metric_data,
                        'relevance': 'high' if query_lower in metric_name.lower() else 'medium'
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:10]  # Return top 10 results
    
    def calculate_metric_target(self, metric_name: str, current_value: float, 
                              industry: str = None) -> Dict[str, Any]:
        """
        Menghitung target untuk metric berdasarkan benchmark
        """
        # This is a simplified example - in practice, you'd have more sophisticated logic
        benchmark_data = self.get_benchmark_data(industry=industry)
        
        if industry and 'industry' in benchmark_data:
            industry_benchmark = benchmark_data['industry'].get(metric_name)
            if industry_benchmark:
                return {
                    'current_value': current_value,
                    'industry_benchmark': industry_benchmark,
                    'performance_vs_benchmark': {
                        'percentage': ((current_value - industry_benchmark) / industry_benchmark) * 100,
                        'status': 'above' if current_value > industry_benchmark else 'below'
                    },
                    'recommended_target': industry_benchmark * 1.1  # 10% above benchmark
                }
        
        return {'error': 'Benchmark data not available for this metric and industry'}
    
    def export_metrics_data(self) -> Dict[str, Any]:
        """
        Export semua data metrics
        """
        return {
            'talent_acquisition_metrics': self.talent_acquisition_metrics,
            'employee_engagement_metrics': self.employee_engagement_metrics,
            'performance_metrics': self.performance_metrics,
            'retention_turnover_metrics': self.retention_turnover_metrics,
            'learning_development_metrics': self.learning_development_metrics,
            'compensation_benefits_metrics': self.compensation_benefits_metrics,
            'diversity_inclusion_metrics': self.diversity_inclusion_metrics,
            'productivity_metrics': self.productivity_metrics,
            'compliance_metrics': self.compliance_metrics,
            'financial_metrics': self.financial_metrics,
            'benchmarking_data': self.benchmarking_data,
            'dashboard_templates': self.dashboard_templates,
            'export_timestamp': datetime.now().isoformat()
        }