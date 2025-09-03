from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class AdvancedHRScenarios:
    """
    Kelas untuk menangani skenario HR yang kompleks dan edge cases
    """
    
    def __init__(self):
        self.complex_scenarios = self._load_complex_scenarios()
        self.edge_cases = self._load_edge_cases()
        self.crisis_management = self._load_crisis_management()
        self.legal_scenarios = self._load_legal_scenarios()
        self.cultural_scenarios = self._load_cultural_scenarios()
        self.remote_work_scenarios = self._load_remote_work_scenarios()
        self.diversity_scenarios = self._load_diversity_scenarios()
        self.change_management = self._load_change_management()
    
    def _load_complex_scenarios(self) -> Dict[str, Any]:
        """
        Skenario HR yang kompleks
        """
        return {
            'layoffs_restructuring': {
                'description': 'Penanganan PHK dan restrukturisasi organisasi',
                'scenarios': [
                    {
                        'situation': 'Mass layoffs due to economic downturn',
                        'considerations': [
                            'Legal compliance with labor laws',
                            'Severance package negotiations',
                            'Communication strategy',
                            'Remaining employee morale',
                            'Outplacement services'
                        ],
                        'best_practices': [
                            'Transparent communication from leadership',
                            'Fair selection criteria',
                            'Adequate notice period',
                            'Support for affected employees',
                            'Retention strategy for key talent'
                        ]
                    },
                    {
                        'situation': 'Department merger and role redundancy',
                        'considerations': [
                            'Skills assessment and mapping',
                            'Cultural integration',
                            'New reporting structures',
                            'Process harmonization',
                            'Change management'
                        ],
                        'best_practices': [
                            'Clear communication about changes',
                            'Retraining opportunities',
                            'Gradual transition timeline',
                            'Regular feedback sessions',
                            'Cultural integration activities'
                        ]
                    }
                ]
            },
            'workplace_investigations': {
                'description': 'Penanganan investigasi workplace misconduct',
                'scenarios': [
                    {
                        'situation': 'Sexual harassment allegations',
                        'process': [
                            'Immediate response and documentation',
                            'Interim protective measures',
                            'Thorough investigation',
                            'Fair hearing process',
                            'Appropriate disciplinary action',
                            'Follow-up and monitoring'
                        ],
                        'legal_requirements': [
                            'Maintain confidentiality',
                            'Prevent retaliation',
                            'Document everything',
                            'Provide support resources',
                            'Ensure fair process'
                        ]
                    },
                    {
                        'situation': 'Fraud or embezzlement investigation',
                        'process': [
                            'Secure evidence and systems',
                            'Involve legal counsel',
                            'Coordinate with authorities',
                            'Internal investigation',
                            'Disciplinary proceedings',
                            'Recovery actions'
                        ],
                        'considerations': [
                            'Criminal vs civil implications',
                            'Insurance coverage',
                            'Reputation management',
                            'System security improvements',
                            'Policy updates'
                        ]
                    }
                ]
            },
            'union_relations': {
                'description': 'Penanganan hubungan dengan serikat pekerja',
                'scenarios': [
                    {
                        'situation': 'Collective bargaining negotiations',
                        'preparation': [
                            'Market research on compensation',
                            'Financial impact analysis',
                            'Legal review of proposals',
                            'Stakeholder alignment',
                            'Communication strategy'
                        ],
                        'negotiation_tactics': [
                            'Interest-based bargaining',
                            'Data-driven proposals',
                            'Creative problem solving',
                            'Relationship building',
                            'Win-win solutions'
                        ]
                    },
                    {
                        'situation': 'Strike or work stoppage',
                        'response_plan': [
                            'Business continuity planning',
                            'Legal compliance review',
                            'Communication with stakeholders',
                            'Security considerations',
                            'Resolution negotiations'
                        ],
                        'prevention_strategies': [
                            'Regular dialogue with union leaders',
                            'Early issue identification',
                            'Grievance process improvement',
                            'Employee engagement initiatives',
                            'Transparent communication'
                        ]
                    }
                ]
            }
        }
    
    def _load_edge_cases(self) -> Dict[str, Any]:
        """
        Edge cases dalam HR
        """
        return {
            'unusual_leave_requests': {
                'scenarios': [
                    {
                        'case': 'Employee requests leave for gender transition',
                        'considerations': [
                            'Legal protections under discrimination laws',
                            'Medical leave requirements',
                            'Workplace accommodation needs',
                            'Privacy and confidentiality',
                            'Team communication strategy'
                        ],
                        'best_practices': [
                            'Consult with legal counsel',
                            'Develop individualized plan',
                            'Ensure workplace safety',
                            'Provide necessary accommodations',
                            'Maintain confidentiality'
                        ]
                    },
                    {
                        'case': 'Employee needs extended leave for family crisis abroad',
                        'considerations': [
                            'FMLA eligibility and limitations',
                            'Personal leave policy flexibility',
                            'Job protection guarantees',
                            'Benefits continuation',
                            'Work arrangement alternatives'
                        ],
                        'options': [
                            'Unpaid personal leave',
                            'Remote work arrangement',
                            'Job sharing or temporary replacement',
                            'Leave of absence with return guarantee',
                            'Flexible schedule upon return'
                        ]
                    }
                ]
            },
            'performance_anomalies': {
                'scenarios': [
                    {
                        'case': 'High performer suddenly declining',
                        'investigation_steps': [
                            'Private conversation with employee',
                            'Review of recent changes or stressors',
                            'Assessment of workload and resources',
                            'Check for personal or health issues',
                            'Evaluate management or team dynamics'
                        ],
                        'intervention_strategies': [
                            'Provide additional support and resources',
                            'Adjust workload or responsibilities',
                            'Offer counseling or EAP services',
                            'Consider temporary role modification',
                            'Develop performance improvement plan'
                        ]
                    },
                    {
                        'case': 'Employee excelling beyond role expectations',
                        'management_approaches': [
                            'Recognize and reward exceptional performance',
                            'Explore advancement opportunities',
                            'Provide stretch assignments',
                            'Consider role expansion or promotion',
                            'Prevent overwork and burnout'
                        ],
                        'retention_strategies': [
                            'Career development planning',
                            'Mentoring opportunities',
                            'Special project assignments',
                            'Leadership development programs',
                            'Compensation review'
                        ]
                    }
                ]
            },
            'technology_challenges': {
                'scenarios': [
                    {
                        'case': 'Employee refuses to use new technology',
                        'assessment': [
                            'Identify root cause of resistance',
                            'Evaluate training adequacy',
                            'Consider accessibility needs',
                            'Assess job requirement changes',
                            'Review accommodation options'
                        ],
                        'solutions': [
                            'Additional training and support',
                            'Gradual implementation approach',
                            'Peer mentoring programs',
                            'Alternative technology options',
                            'Role modification if necessary'
                        ]
                    },
                    {
                        'case': 'Data breach involving employee information',
                        'immediate_response': [
                            'Contain the breach',
                            'Assess scope and impact',
                            'Notify affected employees',
                            'Report to authorities if required',
                            'Implement remediation measures'
                        ],
                        'long_term_actions': [
                            'Review and strengthen security policies',
                            'Provide identity protection services',
                            'Conduct security training',
                            'Update incident response procedures',
                            'Regular security audits'
                        ]
                    }
                ]
            }
        }
    
    def _load_crisis_management(self) -> Dict[str, Any]:
        """
        Manajemen krisis HR
        """
        return {
            'natural_disasters': {
                'preparation': [
                    'Emergency contact database',
                    'Business continuity planning',
                    'Remote work capabilities',
                    'Communication systems backup',
                    'Employee safety protocols'
                ],
                'response': [
                    'Employee safety verification',
                    'Activate emergency communication',
                    'Assess workplace damage',
                    'Implement business continuity plan',
                    'Provide employee assistance'
                ],
                'recovery': [
                    'Workplace restoration planning',
                    'Employee support services',
                    'Gradual return to normal operations',
                    'Lessons learned documentation',
                    'Plan updates and improvements'
                ]
            },
            'pandemic_response': {
                'health_safety': [
                    'Health screening protocols',
                    'Workplace sanitization procedures',
                    'Personal protective equipment',
                    'Social distancing measures',
                    'Contact tracing procedures'
                ],
                'work_arrangements': [
                    'Remote work implementation',
                    'Flexible scheduling options',
                    'Hybrid work models',
                    'Technology support',
                    'Performance management adaptation'
                ],
                'employee_support': [
                    'Mental health resources',
                    'Childcare assistance',
                    'Financial support programs',
                    'Communication and updates',
                    'Return-to-work planning'
                ]
            },
            'workplace_violence': {
                'prevention': [
                    'Threat assessment procedures',
                    'Employee screening processes',
                    'Workplace security measures',
                    'Training and awareness programs',
                    'Reporting mechanisms'
                ],
                'response': [
                    'Immediate safety measures',
                    'Law enforcement coordination',
                    'Employee evacuation procedures',
                    'Crisis communication',
                    'Incident documentation'
                ],
                'aftermath': [
                    'Employee counseling services',
                    'Workplace security review',
                    'Policy and procedure updates',
                    'Training program enhancement',
                    'Long-term support planning'
                ]
            }
        }
    
    def _load_legal_scenarios(self) -> Dict[str, Any]:
        """
        Skenario legal HR
        """
        return {
            'discrimination_claims': {
                'types': [
                    'Age discrimination',
                    'Gender discrimination',
                    'Racial discrimination',
                    'Religious discrimination',
                    'Disability discrimination',
                    'Sexual orientation discrimination'
                ],
                'prevention_strategies': [
                    'Comprehensive anti-discrimination policies',
                    'Regular training programs',
                    'Fair hiring and promotion practices',
                    'Diverse interview panels',
                    'Objective performance criteria'
                ],
                'response_procedures': [
                    'Immediate investigation',
                    'Documentation of findings',
                    'Appropriate corrective action',
                    'Legal counsel consultation',
                    'Follow-up monitoring'
                ]
            },
            'wage_hour_compliance': {
                'common_issues': [
                    'Overtime calculation errors',
                    'Meal and rest break violations',
                    'Misclassification of employees',
                    'Off-the-clock work',
                    'Minimum wage compliance'
                ],
                'compliance_measures': [
                    'Accurate time tracking systems',
                    'Regular policy reviews',
                    'Manager training on labor laws',
                    'Audit of pay practices',
                    'Clear work hour policies'
                ]
            },
            'privacy_rights': {
                'employee_monitoring': [
                    'Computer and internet usage',
                    'Email and communication monitoring',
                    'Video surveillance',
                    'GPS tracking',
                    'Social media monitoring'
                ],
                'legal_requirements': [
                    'Notice and consent requirements',
                    'Legitimate business purpose',
                    'Proportionality of monitoring',
                    'Data protection compliance',
                    'Employee privacy expectations'
                ]
            }
        }
    
    def _load_cultural_scenarios(self) -> Dict[str, Any]:
        """
        Skenario budaya dan keberagaman
        """
        return {
            'religious_accommodations': {
                'common_requests': [
                    'Prayer time and space',
                    'Religious holiday observance',
                    'Dress code modifications',
                    'Dietary restrictions',
                    'Schedule adjustments'
                ],
                'accommodation_process': [
                    'Interactive dialogue with employee',
                    'Assessment of accommodation options',
                    'Undue hardship evaluation',
                    'Implementation of reasonable accommodation',
                    'Ongoing monitoring and adjustment'
                ]
            },
            'cultural_conflicts': {
                'scenarios': [
                    {
                        'situation': 'Communication style differences',
                        'interventions': [
                            'Cultural awareness training',
                            'Communication skills workshops',
                            'Mediation sessions',
                            'Team building activities',
                            'Clear communication guidelines'
                        ]
                    },
                    {
                        'situation': 'Holiday and celebration conflicts',
                        'solutions': [
                            'Inclusive holiday policies',
                            'Flexible time-off options',
                            'Cultural celebration calendar',
                            'Respectful workplace guidelines',
                            'Employee resource groups'
                        ]
                    }
                ]
            },
            'language_barriers': {
                'challenges': [
                    'Safety communication',
                    'Performance feedback',
                    'Training effectiveness',
                    'Team collaboration',
                    'Customer service quality'
                ],
                'solutions': [
                    'Language training programs',
                    'Translation services',
                    'Multilingual materials',
                    'Buddy system implementation',
                    'Visual communication tools'
                ]
            }
        }
    
    def _load_remote_work_scenarios(self) -> Dict[str, Any]:
        """
        Skenario remote work
        """
        return {
            'performance_management': {
                'challenges': [
                    'Measuring productivity remotely',
                    'Maintaining team cohesion',
                    'Providing feedback and coaching',
                    'Career development opportunities',
                    'Work-life balance monitoring'
                ],
                'best_practices': [
                    'Results-oriented performance metrics',
                    'Regular check-ins and one-on-ones',
                    'Virtual team building activities',
                    'Clear communication expectations',
                    'Flexible work arrangements'
                ]
            },
            'technology_support': {
                'requirements': [
                    'Reliable internet connectivity',
                    'Appropriate hardware and software',
                    'Cybersecurity measures',
                    'Technical support availability',
                    'Data backup and recovery'
                ],
                'policies': [
                    'Equipment provision and maintenance',
                    'Expense reimbursement guidelines',
                    'Security and privacy protocols',
                    'Acceptable use policies',
                    'Troubleshooting procedures'
                ]
            },
            'legal_compliance': {
                'considerations': [
                    'Workers compensation coverage',
                    'Wage and hour compliance',
                    'Tax implications',
                    'International employment laws',
                    'Data protection regulations'
                ],
                'documentation': [
                    'Remote work agreements',
                    'Time tracking requirements',
                    'Workspace safety assessments',
                    'Policy acknowledgments',
                    'Performance expectations'
                ]
            }
        }
    
    def _load_diversity_scenarios(self) -> Dict[str, Any]:
        """
        Skenario diversity dan inclusion
        """
        return {
            'inclusive_hiring': {
                'strategies': [
                    'Diverse sourcing channels',
                    'Bias-free job descriptions',
                    'Structured interview processes',
                    'Diverse interview panels',
                    'Objective selection criteria'
                ],
                'metrics': [
                    'Diversity in candidate pipeline',
                    'Hiring manager training completion',
                    'Time-to-hire by demographic',
                    'Offer acceptance rates',
                    'New hire diversity statistics'
                ]
            },
            'workplace_inclusion': {
                'initiatives': [
                    'Employee resource groups',
                    'Mentorship programs',
                    'Inclusive leadership training',
                    'Bias interruption workshops',
                    'Cultural competency development'
                ],
                'measurement': [
                    'Inclusion survey results',
                    'Employee engagement scores',
                    'Retention rates by demographic',
                    'Promotion and advancement rates',
                    'Pay equity analysis'
                ]
            },
            'accessibility_accommodations': {
                'physical_accommodations': [
                    'Wheelchair accessibility',
                    'Ergonomic workstations',
                    'Assistive technology',
                    'Modified work schedules',
                    'Accessible parking and facilities'
                ],
                'cognitive_accommodations': [
                    'Written instructions and procedures',
                    'Extended time for tasks',
                    'Quiet work environments',
                    'Flexible break schedules',
                    'Job coaching support'
                ]
            }
        }
    
    def _load_change_management(self) -> Dict[str, Any]:
        """
        Manajemen perubahan organisasi
        """
        return {
            'organizational_restructuring': {
                'phases': [
                    {
                        'phase': 'Planning and Preparation',
                        'activities': [
                            'Stakeholder analysis',
                            'Change impact assessment',
                            'Communication strategy development',
                            'Resource allocation planning',
                            'Risk mitigation strategies'
                        ]
                    },
                    {
                        'phase': 'Implementation',
                        'activities': [
                            'Leadership alignment',
                            'Employee communication',
                            'Training and development',
                            'Process redesign',
                            'Performance monitoring'
                        ]
                    },
                    {
                        'phase': 'Reinforcement',
                        'activities': [
                            'Feedback collection',
                            'Adjustment and refinement',
                            'Success celebration',
                            'Lessons learned documentation',
                            'Sustainability planning'
                        ]
                    }
                ]
            },
            'culture_transformation': {
                'elements': [
                    'Values definition and alignment',
                    'Behavior modeling by leaders',
                    'Recognition and reward systems',
                    'Communication and storytelling',
                    'Measurement and feedback'
                ],
                'timeline': [
                    'Assessment and baseline (3-6 months)',
                    'Design and planning (6-12 months)',
                    'Implementation (12-24 months)',
                    'Reinforcement (ongoing)',
                    'Evaluation and adjustment (quarterly)'
                ]
            },
            'technology_adoption': {
                'success_factors': [
                    'User-centered design',
                    'Comprehensive training programs',
                    'Change champion network',
                    'Continuous support and feedback',
                    'Phased rollout approach'
                ],
                'resistance_management': [
                    'Identify and address concerns',
                    'Provide adequate training and support',
                    'Communicate benefits clearly',
                    'Involve users in design process',
                    'Celebrate early wins and successes'
                ]
            }
        }
    
    def search_scenario(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Mencari skenario berdasarkan query
        """
        results = []
        query_lower = query.lower()
        
        # Tentukan kategori yang akan dicari
        search_categories = [category] if category else [
            'complex_scenarios', 'edge_cases', 'crisis_management',
            'legal_scenarios', 'cultural_scenarios', 'remote_work_scenarios',
            'diversity_scenarios', 'change_management'
        ]
        
        for cat in search_categories:
            if hasattr(self, cat):
                data = getattr(self, cat)
                matches = self._search_in_data(data, query_lower)
                for match in matches:
                    results.append({
                        'category': cat,
                        'relevance': match['relevance'],
                        'data': match['data'],
                        'context': match.get('context', '')
                    })
        
        return sorted(results, key=lambda x: x['relevance'], reverse=True)
    
    def _search_in_data(self, data: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """
        Mencari dalam data dengan scoring relevance
        """
        results = []
        
        def search_recursive(obj, path="", relevance=0.0):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_lower = key.lower()
                    if query in key_lower:
                        relevance += 0.8
                    search_recursive(value, f"{path}.{key}" if path else key, relevance)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_recursive(item, f"{path}[{i}]", relevance)
            elif isinstance(obj, str):
                obj_lower = obj.lower()
                if query in obj_lower:
                    relevance += 0.6
                    results.append({
                        'relevance': relevance,
                        'data': obj,
                        'context': path
                    })
        
        search_recursive(data)
        return results
    
    def get_scenario_by_type(self, scenario_type: str) -> Dict[str, Any]:
        """
        Mendapatkan skenario berdasarkan tipe
        """
        scenario_map = {
            'layoffs': self.complex_scenarios.get('layoffs_restructuring', {}),
            'investigation': self.complex_scenarios.get('workplace_investigations', {}),
            'union': self.complex_scenarios.get('union_relations', {}),
            'crisis': self.crisis_management,
            'legal': self.legal_scenarios,
            'cultural': self.cultural_scenarios,
            'remote': self.remote_work_scenarios,
            'diversity': self.diversity_scenarios,
            'change': self.change_management
        }
        return scenario_map.get(scenario_type, {})
    
    def export_all_scenarios(self) -> Dict[str, Any]:
        """
        Export semua skenario
        """
        return {
            'complex_scenarios': self.complex_scenarios,
            'edge_cases': self.edge_cases,
            'crisis_management': self.crisis_management,
            'legal_scenarios': self.legal_scenarios,
            'cultural_scenarios': self.cultural_scenarios,
            'remote_work_scenarios': self.remote_work_scenarios,
            'diversity_scenarios': self.diversity_scenarios,
            'change_management': self.change_management,
            'export_timestamp': datetime.now().isoformat()
        }