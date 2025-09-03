# -*- coding: utf-8 -*-
"""
Data Domain HR yang Komprehensif
Berisi informasi mendalam tentang berbagai aspek HR dan kepegawaian
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class HRDomainData:
    """
    Kelas untuk mengelola data domain HR yang komprehensif
    """
    
    def __init__(self):
        self.employee_lifecycle = self._load_employee_lifecycle_data()
        self.compensation_benefits = self._load_compensation_benefits_data()
        self.performance_management = self._load_performance_management_data()
        self.learning_development = self._load_learning_development_data()
        self.compliance_policies = self._load_compliance_policies_data()
        self.organizational_structure = self._load_organizational_structure_data()
        self.hr_processes = self._load_hr_processes_data()
        self.employee_relations = self._load_employee_relations_data()
    
    def _load_employee_lifecycle_data(self) -> Dict[str, Any]:
        """
        Data lengkap tentang siklus hidup karyawan
        """
        return {
            'recruitment': {
                'process_stages': [
                    {
                        'stage': 'Job Posting',
                        'duration': '1-2 weeks',
                        'activities': ['Create job description', 'Post on job boards', 'Internal announcement'],
                        'stakeholders': ['Hiring Manager', 'HR Recruiter'],
                        'deliverables': ['Job posting', 'Candidate sourcing plan']
                    },
                    {
                        'stage': 'Application Screening',
                        'duration': '1 week',
                        'activities': ['Resume review', 'Initial screening', 'ATS filtering'],
                        'stakeholders': ['HR Recruiter', 'Hiring Manager'],
                        'deliverables': ['Shortlisted candidates', 'Screening notes']
                    },
                    {
                        'stage': 'Interview Process',
                        'duration': '2-3 weeks',
                        'activities': ['Phone screening', 'Technical interview', 'Panel interview', 'Final interview'],
                        'stakeholders': ['Hiring Manager', 'Team Members', 'HR Business Partner'],
                        'deliverables': ['Interview feedback', 'Candidate evaluation']
                    },
                    {
                        'stage': 'Background Check',
                        'duration': '1-2 weeks',
                        'activities': ['Reference check', 'Education verification', 'Criminal background check'],
                        'stakeholders': ['HR Operations', 'Third-party vendor'],
                        'deliverables': ['Background check report', 'Reference feedback']
                    },
                    {
                        'stage': 'Job Offer',
                        'duration': '1 week',
                        'activities': ['Salary negotiation', 'Offer letter preparation', 'Contract signing'],
                        'stakeholders': ['HR Business Partner', 'Hiring Manager', 'Legal'],
                        'deliverables': ['Signed offer letter', 'Employment contract']
                    }
                ],
                'common_questions': [
                    {
                        'question': 'Berapa lama proses recruitment biasanya?',
                        'answer': 'Proses recruitment end-to-end biasanya memakan waktu 6-8 minggu, tergantung kompleksitas posisi dan ketersediaan kandidat.',
                        'details': 'Timeline bisa lebih cepat untuk posisi junior (4-6 minggu) atau lebih lama untuk posisi senior/specialized (8-12 minggu).'
                    },
                    {
                        'question': 'Apa saja tahapan interview yang harus dilalui?',
                        'answer': 'Tahapan interview meliputi: 1) Phone screening dengan HR, 2) Technical interview dengan tim, 3) Panel interview dengan stakeholders, 4) Final interview dengan hiring manager.',
                        'details': 'Untuk posisi tertentu mungkin ada additional assessment seperti case study, presentation, atau practical test.'
                    }
                ],
                'metrics': {
                    'time_to_hire': '45 days average',
                    'cost_per_hire': 'Rp 15,000,000 average',
                    'offer_acceptance_rate': '85%',
                    'quality_of_hire': '4.2/5.0'
                }
            },
            
            'onboarding': {
                'pre_boarding': {
                    'timeline': '1 week before start date',
                    'activities': [
                        'Send welcome email with first day info',
                        'Prepare workspace and equipment',
                        'Create system accounts and access',
                        'Schedule orientation sessions',
                        'Assign buddy/mentor'
                    ],
                    'documents': [
                        'Employee handbook',
                        'Organizational chart',
                        'First week schedule',
                        'IT setup guide',
                        'Parking and facility info'
                    ]
                },
                'first_day': {
                    'timeline': 'Day 1',
                    'activities': [
                        'Welcome and office tour',
                        'HR orientation session',
                        'IT setup and system training',
                        'Meet team and key stakeholders',
                        'Complete mandatory paperwork'
                    ],
                    'deliverables': [
                        'Signed employment documents',
                        'Emergency contact information',
                        'Bank account details for payroll',
                        'Benefits enrollment forms',
                        'ID photo and badge creation'
                    ]
                },
                'first_week': {
                    'timeline': 'Days 2-5',
                    'activities': [
                        'Department-specific orientation',
                        'Role-specific training',
                        'Shadow experienced team members',
                        'Complete compliance training',
                        'Set initial goals and expectations'
                    ],
                    'checkpoints': [
                        'Daily check-ins with manager',
                        'Buddy system feedback',
                        'HR follow-up call',
                        'IT systems functionality check'
                    ]
                },
                'first_month': {
                    'timeline': 'Weeks 2-4',
                    'activities': [
                        'Begin actual work assignments',
                        'Attend relevant meetings',
                        'Complete required certifications',
                        'Build relationships with colleagues',
                        'Receive ongoing feedback'
                    ],
                    'milestones': [
                        '30-day check-in meeting',
                        'Initial performance feedback',
                        'Benefits enrollment completion',
                        'Training completion certificates'
                    ]
                },
                'probation_period': {
                    'duration': '3 months',
                    'evaluation_points': ['30 days', '60 days', '90 days'],
                    'criteria': [
                        'Job performance and quality of work',
                        'Adherence to company policies',
                        'Team integration and collaboration',
                        'Learning agility and adaptability',
                        'Attendance and punctuality'
                    ],
                    'outcomes': [
                        'Confirmation of employment',
                        'Extended probation (rare cases)',
                        'Termination (performance issues)'
                    ]
                }
            },
            
            'career_development': {
                'career_paths': {
                    'individual_contributor': {
                        'levels': ['Junior', 'Mid-level', 'Senior', 'Principal', 'Distinguished'],
                        'progression_criteria': [
                            'Technical expertise and skill development',
                            'Problem-solving capability',
                            'Mentoring and knowledge sharing',
                            'Innovation and thought leadership',
                            'Cross-functional collaboration'
                        ]
                    },
                    'management_track': {
                        'levels': ['Team Lead', 'Manager', 'Senior Manager', 'Director', 'VP'],
                        'progression_criteria': [
                            'People management skills',
                            'Strategic thinking and planning',
                            'Business acumen',
                            'Change management capability',
                            'Organizational leadership'
                        ]
                    }
                },
                'development_programs': [
                    {
                        'program': 'Leadership Development Program',
                        'target': 'High-potential employees',
                        'duration': '12 months',
                        'components': ['Executive coaching', 'Cross-functional projects', 'Mentorship', '360-degree feedback']
                    },
                    {
                        'program': 'Technical Excellence Program',
                        'target': 'Senior individual contributors',
                        'duration': '6 months',
                        'components': ['Advanced technical training', 'Conference attendance', 'Innovation projects', 'Knowledge sharing sessions']
                    }
                ]
            },
            
            'offboarding': {
                'resignation_process': {
                    'notice_period': {
                        'junior_level': '1 month',
                        'senior_level': '2 months',
                        'management': '3 months'
                    },
                    'exit_interview': {
                        'timing': 'Last week of employment',
                        'conducted_by': 'HR Business Partner',
                        'topics': [
                            'Reason for leaving',
                            'Job satisfaction feedback',
                            'Manager relationship',
                            'Company culture assessment',
                            'Suggestions for improvement'
                        ]
                    }
                },
                'knowledge_transfer': {
                    'documentation': [
                        'Project handover notes',
                        'Process documentation',
                        'Contact lists and relationships',
                        'Ongoing commitments and deadlines'
                    ],
                    'training': [
                        'Shadow sessions with replacement',
                        'Knowledge sharing meetings',
                        'System access and passwords transfer'
                    ]
                },
                'final_settlement': {
                    'components': [
                        'Final salary payment',
                        'Unused leave encashment',
                        'Bonus and incentive payments',
                        'Expense reimbursements',
                        'Severance pay (if applicable)'
                    ],
                    'deductions': [
                        'Notice period shortfall',
                        'Company property not returned',
                        'Outstanding loans or advances',
                        'Training cost recovery (if applicable)'
                    ]
                }
            }
        }
    
    def _load_compensation_benefits_data(self) -> Dict[str, Any]:
        """
        Data komprehensif tentang kompensasi dan benefit
        """
        return {
            'salary_structure': {
                'components': {
                    'basic_salary': {
                        'description': 'Fixed monthly salary component',
                        'percentage': '60-70% of total compensation',
                        'tax_treatment': 'Fully taxable',
                        'frequency': 'Monthly'
                    },
                    'allowances': {
                        'transport_allowance': {
                            'amount': 'Rp 500,000 - 1,500,000',
                            'eligibility': 'All employees',
                            'tax_treatment': 'Tax-free up to Rp 1,320,000'
                        },
                        'meal_allowance': {
                            'amount': 'Rp 300,000 - 800,000',
                            'eligibility': 'All employees',
                            'tax_treatment': 'Tax-free up to Rp 1,320,000'
                        },
                        'communication_allowance': {
                            'amount': 'Rp 200,000 - 500,000',
                            'eligibility': 'Based on role requirements',
                            'tax_treatment': 'Taxable'
                        }
                    },
                    'variable_pay': {
                        'performance_bonus': {
                            'frequency': 'Quarterly/Annual',
                            'calculation': 'Based on individual and company performance',
                            'range': '0-30% of annual basic salary'
                        },
                        'sales_commission': {
                            'eligibility': 'Sales roles only',
                            'structure': 'Tiered commission rates',
                            'payment': 'Monthly based on achieved sales'
                        }
                    }
                },
                'salary_bands': {
                    'junior_level': {
                        'range': 'Rp 8,000,000 - 15,000,000',
                        'experience': '0-3 years',
                        'education': 'Bachelor degree or equivalent'
                    },
                    'mid_level': {
                        'range': 'Rp 15,000,000 - 25,000,000',
                        'experience': '3-7 years',
                        'education': 'Bachelor degree + relevant experience'
                    },
                    'senior_level': {
                        'range': 'Rp 25,000,000 - 40,000,000',
                        'experience': '7-12 years',
                        'education': 'Bachelor/Master degree + extensive experience'
                    },
                    'management': {
                        'range': 'Rp 40,000,000 - 80,000,000',
                        'experience': '10+ years with management experience',
                        'education': 'Bachelor/Master degree + leadership experience'
                    }
                }
            },
            
            'benefits_package': {
                'mandatory_benefits': {
                    'jamsostek': {
                        'components': ['JKK', 'JKM', 'JHT', 'JP'],
                        'employee_contribution': '2% of salary (JHT) + 1% (JP)',
                        'employer_contribution': '3.7% of salary (total)',
                        'coverage': 'All permanent employees'
                    },
                    'bpjs_kesehatan': {
                        'employee_contribution': '1% of salary',
                        'employer_contribution': '4% of salary',
                        'coverage': 'Employee + 3 family members',
                        'benefits': 'Comprehensive healthcare coverage'
                    }
                },
                'company_benefits': {
                    'health_insurance': {
                        'provider': 'Private insurance company',
                        'coverage': 'Employee + spouse + 2 children',
                        'annual_limit': 'Rp 100,000,000 per person',
                        'features': ['Cashless treatment', 'Outpatient', 'Inpatient', 'Dental', 'Optical']
                    },
                    'life_insurance': {
                        'coverage': '24x monthly basic salary',
                        'beneficiary': 'Designated by employee',
                        'additional_coverage': 'Accidental death and dismemberment'
                    },
                    'annual_leave': {
                        'entitlement': '12 days per year',
                        'accrual': '1 day per month',
                        'carry_forward': 'Maximum 6 days to next year',
                        'encashment': 'Allowed for unused leave at year-end'
                    },
                    'sick_leave': {
                        'entitlement': '12 days per year',
                        'medical_certificate': 'Required for >2 consecutive days',
                        'extended_sick_leave': 'Up to 6 months with medical board approval'
                    },
                    'maternity_leave': {
                        'duration': '3 months (90 days)',
                        'salary': '100% of basic salary',
                        'additional_benefits': 'Lactation room access, flexible hours'
                    },
                    'paternity_leave': {
                        'duration': '2 days',
                        'salary': '100% of basic salary',
                        'timing': 'Within 30 days of child birth'
                    }
                },
                'perks_and_facilities': {
                    'flexible_working': {
                        'work_from_home': 'Up to 2 days per week',
                        'flexible_hours': 'Core hours 10 AM - 3 PM',
                        'compressed_workweek': 'Available for certain roles'
                    },
                    'learning_budget': {
                        'annual_allowance': 'Rp 5,000,000 per employee',
                        'eligible_expenses': ['Training courses', 'Conferences', 'Certifications', 'Books'],
                        'approval_process': 'Manager and HR approval required'
                    },
                    'wellness_program': {
                        'gym_membership': 'Subsidized membership',
                        'health_checkup': 'Annual comprehensive health screening',
                        'mental_health': 'Employee assistance program (EAP)'
                    },
                    'employee_discounts': {
                        'company_products': '20% discount',
                        'partner_merchants': 'Various discounts and cashback',
                        'group_insurance': 'Discounted rates for additional coverage'
                    }
                }
            },
            
            'compensation_philosophy': {
                'market_positioning': {
                    'target': '50th-75th percentile of market',
                    'benchmark_sources': ['Willis Towers Watson', 'Mercer', 'Aon Hewitt'],
                    'review_frequency': 'Annual market study'
                },
                'pay_for_performance': {
                    'principle': 'Differentiated rewards based on performance',
                    'performance_ratings': {
                        'exceeds_expectations': 'Salary increase 8-12%',
                        'meets_expectations': 'Salary increase 4-6%',
                        'below_expectations': 'Salary increase 0-2%'
                    }
                },
                'internal_equity': {
                    'job_evaluation': 'Point-factor method',
                    'salary_ranges': 'Defined for each job level',
                    'compression_ratio': 'Maximum 1.5x between min and max'
                }
            }
        }
    
    def _load_performance_management_data(self) -> Dict[str, Any]:
        """
        Data lengkap tentang manajemen kinerja
        """
        return {
            'performance_cycle': {
                'annual_cycle': {
                    'goal_setting': {
                        'timing': 'January - February',
                        'process': 'Cascading from company to individual goals',
                        'framework': 'OKR (Objectives and Key Results)',
                        'components': [
                            'Business objectives alignment',
                            'Individual development goals',
                            'Behavioral competencies',
                            'Key performance indicators'
                        ]
                    },
                    'mid_year_review': {
                        'timing': 'June - July',
                        'purpose': 'Progress check and course correction',
                        'activities': [
                            'Goal progress assessment',
                            'Feedback exchange',
                            'Development plan update',
                            'Support needs identification'
                        ]
                    },
                    'year_end_review': {
                        'timing': 'November - December',
                        'components': [
                            'Self-assessment completion',
                            'Manager evaluation',
                            'Peer feedback (360-degree)',
                            'Calibration sessions',
                            'Final rating and feedback'
                        ]
                    }
                },
                'continuous_feedback': {
                    'one_on_ones': {
                        'frequency': 'Weekly or bi-weekly',
                        'duration': '30-60 minutes',
                        'agenda': [
                            'Work progress and challenges',
                            'Goal alignment and priorities',
                            'Development opportunities',
                            'Feedback and recognition'
                        ]
                    },
                    'real_time_feedback': {
                        'tools': 'Performance management system',
                        'types': ['Praise', 'Constructive feedback', 'Coaching'],
                        'frequency': 'Ongoing as needed'
                    }
                }
            },
            
            'performance_ratings': {
                'rating_scale': {
                    '5_exceptional': {
                        'description': 'Consistently exceeds expectations and delivers exceptional results',
                        'percentage': '5-10% of population',
                        'characteristics': [
                            'Significantly exceeds all goals',
                            'Demonstrates exceptional competencies',
                            'Serves as role model for others',
                            'Drives innovation and improvement'
                        ]
                    },
                    '4_exceeds': {
                        'description': 'Frequently exceeds expectations and delivers strong results',
                        'percentage': '15-25% of population',
                        'characteristics': [
                            'Exceeds most goals',
                            'Strong demonstration of competencies',
                            'Contributes beyond core responsibilities',
                            'Supports team and organizational success'
                        ]
                    },
                    '3_meets': {
                        'description': 'Consistently meets expectations and delivers solid results',
                        'percentage': '50-60% of population',
                        'characteristics': [
                            'Achieves all key goals',
                            'Demonstrates required competencies',
                            'Fulfills job responsibilities effectively',
                            'Contributes positively to team'
                        ]
                    },
                    '2_partially_meets': {
                        'description': 'Sometimes meets expectations but has areas for improvement',
                        'percentage': '10-15% of population',
                        'characteristics': [
                            'Achieves some but not all goals',
                            'Inconsistent competency demonstration',
                            'Requires additional support and guidance',
                            'Shows potential for improvement'
                        ]
                    },
                    '1_does_not_meet': {
                        'description': 'Does not meet expectations and requires significant improvement',
                        'percentage': '5% of population',
                        'characteristics': [
                            'Fails to achieve key goals',
                            'Below standard competency levels',
                            'Requires performance improvement plan',
                            'May face employment consequences'
                        ]
                    }
                },
                'calibration_process': {
                    'purpose': 'Ensure consistent and fair rating distribution',
                    'participants': 'Managers and HR Business Partners',
                    'process': [
                        'Initial manager ratings',
                        'Peer manager review',
                        'Calibration discussion',
                        'Final rating confirmation'
                    ]
                }
            },
            
            'development_planning': {
                'competency_framework': {
                    'core_competencies': [
                        {
                            'competency': 'Customer Focus',
                            'definition': 'Anticipates, understands and responds to customer needs',
                            'behavioral_indicators': [
                                'Seeks to understand customer requirements',
                                'Delivers solutions that meet customer needs',
                                'Builds strong customer relationships',
                                'Goes extra mile to ensure customer satisfaction'
                            ]
                        },
                        {
                            'competency': 'Innovation',
                            'definition': 'Generates creative solutions and embraces new approaches',
                            'behavioral_indicators': [
                                'Challenges conventional thinking',
                                'Generates creative and practical solutions',
                                'Embraces change and new technologies',
                                'Encourages innovation in others'
                            ]
                        },
                        {
                            'competency': 'Collaboration',
                            'definition': 'Works effectively with others to achieve common goals',
                            'behavioral_indicators': [
                                'Builds positive working relationships',
                                'Shares knowledge and resources',
                                'Supports team decisions and goals',
                                'Resolves conflicts constructively'
                            ]
                        }
                    ],
                    'leadership_competencies': [
                        {
                            'competency': 'Strategic Thinking',
                            'definition': 'Develops long-term vision and strategic direction',
                            'behavioral_indicators': [
                                'Analyzes market trends and opportunities',
                                'Develops comprehensive strategic plans',
                                'Aligns team activities with strategic goals',
                                'Anticipates future challenges and opportunities'
                            ]
                        },
                        {
                            'competency': 'People Development',
                            'definition': 'Develops and empowers team members',
                            'behavioral_indicators': [
                                'Provides regular coaching and feedback',
                                'Creates development opportunities',
                                'Recognizes and rewards good performance',
                                'Builds succession pipeline'
                            ]
                        }
                    ]
                },
                'development_methods': {
                    '70_20_10_model': {
                        'on_the_job': {
                            'percentage': '70%',
                            'methods': [
                                'Stretch assignments',
                                'Cross-functional projects',
                                'Job rotation',
                                'Acting roles',
                                'Special initiatives'
                            ]
                        },
                        'social_learning': {
                            'percentage': '20%',
                            'methods': [
                                'Mentoring and coaching',
                                'Peer learning groups',
                                'Communities of practice',
                                'Reverse mentoring',
                                'Action learning sets'
                            ]
                        },
                        'formal_learning': {
                            'percentage': '10%',
                            'methods': [
                                'Training programs',
                                'Workshops and seminars',
                                'Online courses',
                                'Conferences and events',
                                'Certification programs'
                            ]
                        }
                    }
                }
            },
            
            'performance_improvement': {
                'pip_process': {
                    'triggers': [
                        'Performance rating below expectations',
                        'Consistent failure to meet goals',
                        'Behavioral issues affecting performance',
                        'Skills gap impacting job performance'
                    ],
                    'duration': '90 days (extendable to 180 days)',
                    'components': [
                        'Clear performance expectations',
                        'Specific improvement goals',
                        'Regular check-in meetings',
                        'Additional training and support',
                        'Timeline for improvement'
                    ],
                    'outcomes': [
                        'Successful completion and continued employment',
                        'Partial improvement with extended PIP',
                        'Unsuccessful completion leading to termination'
                    ]
                },
                'support_mechanisms': {
                    'coaching': 'Professional coaching for skill development',
                    'training': 'Targeted training programs',
                    'mentoring': 'Pairing with experienced colleague',
                    'job_redesign': 'Adjusting role to better fit capabilities',
                    'transfer': 'Moving to more suitable position'
                }
            }
        }
    
    def _load_learning_development_data(self) -> Dict[str, Any]:
        """
        Data komprehensif tentang pembelajaran dan pengembangan
        """
        return {
            'learning_strategy': {
                'vision': 'Create a culture of continuous learning and development',
                'objectives': [
                    'Build critical skills for business success',
                    'Develop future leaders',
                    'Enhance employee engagement and retention',
                    'Foster innovation and adaptability'
                ],
                'principles': [
                    'Learner-centric approach',
                    'Just-in-time learning',
                    'Blended learning methodology',
                    'Measurement and continuous improvement'
                ]
            },
            
            'learning_programs': {
                'onboarding_program': {
                    'duration': '3 months',
                    'modules': [
                        {
                            'module': 'Company Orientation',
                            'duration': '1 day',
                            'content': ['Company history and values', 'Organizational structure', 'Policies and procedures']
                        },
                        {
                            'module': 'Role-specific Training',
                            'duration': '2 weeks',
                            'content': ['Job responsibilities', 'Systems and tools', 'Process workflows']
                        },
                        {
                            'module': 'Compliance Training',
                            'duration': '1 week',
                            'content': ['Code of conduct', 'Safety procedures', 'Data privacy', 'Anti-harassment']
                        }
                    ]
                },
                
                'technical_skills': {
                    'programming': {
                        'languages': ['Python', 'Java', 'JavaScript', 'C#', 'Go'],
                        'frameworks': ['React', 'Angular', 'Spring Boot', 'Django', 'Node.js'],
                        'delivery_methods': ['Online courses', 'Bootcamps', 'Workshops', 'Peer programming']
                    },
                    'data_analytics': {
                        'tools': ['SQL', 'Python/R', 'Tableau', 'Power BI', 'Excel Advanced'],
                        'concepts': ['Statistical analysis', 'Machine learning', 'Data visualization', 'Business intelligence'],
                        'certifications': ['Google Analytics', 'Microsoft Power BI', 'Tableau Desktop']
                    },
                    'cloud_technologies': {
                        'platforms': ['AWS', 'Azure', 'Google Cloud'],
                        'services': ['Computing', 'Storage', 'Networking', 'Databases', 'AI/ML'],
                        'certifications': ['AWS Solutions Architect', 'Azure Fundamentals', 'Google Cloud Professional']
                    }
                },
                
                'soft_skills': {
                    'communication': {
                        'programs': [
                            'Effective Presentation Skills',
                            'Business Writing',
                            'Cross-cultural Communication',
                            'Difficult Conversations'
                        ],
                        'delivery': ['Workshops', 'Role-playing', 'Video analysis', 'Peer feedback']
                    },
                    'leadership': {
                        'programs': [
                            'First-time Manager Program',
                            'Advanced Leadership Skills',
                            'Strategic Leadership',
                            'Change Management'
                        ],
                        'methods': ['Action learning', 'Executive coaching', '360-degree feedback', 'Mentoring']
                    },
                    'project_management': {
                        'methodologies': ['Agile/Scrum', 'Waterfall', 'Lean', 'Six Sigma'],
                        'certifications': ['PMP', 'Scrum Master', 'Lean Six Sigma'],
                        'tools': ['Jira', 'Trello', 'Microsoft Project', 'Asana']
                    }
                },
                
                'leadership_development': {
                    'emerging_leaders': {
                        'target': 'High-potential individual contributors',
                        'duration': '6 months',
                        'components': [
                            'Leadership assessment',
                            'Core leadership skills training',
                            'Cross-functional project',
                            'Executive mentoring',
                            'Presentation to senior leadership'
                        ]
                    },
                    'new_managers': {
                        'target': 'First-time people managers',
                        'duration': '12 months',
                        'components': [
                            'Management fundamentals',
                            'Performance management',
                            'Team building and motivation',
                            'Coaching and feedback skills',
                            'Business acumen'
                        ]
                    },
                    'senior_leaders': {
                        'target': 'Directors and above',
                        'duration': 'Ongoing',
                        'components': [
                            'Strategic thinking',
                            'Executive presence',
                            'Change leadership',
                            'Board readiness',
                            'Industry thought leadership'
                        ]
                    }
                }
            },
            
            'learning_delivery': {
                'modalities': {
                    'instructor_led': {
                        'formats': ['Classroom training', 'Workshops', 'Seminars', 'Conferences'],
                        'benefits': ['Interactive learning', 'Immediate feedback', 'Networking opportunities'],
                        'challenges': ['Scheduling conflicts', 'Travel costs', 'Limited scalability']
                    },
                    'virtual_learning': {
                        'formats': ['Webinars', 'Virtual classrooms', 'Online workshops'],
                        'benefits': ['Cost-effective', 'Flexible scheduling', 'Global reach'],
                        'challenges': ['Technology requirements', 'Engagement challenges', 'Limited interaction']
                    },
                    'e_learning': {
                        'formats': ['Online courses', 'Microlearning', 'Mobile learning', 'Gamification'],
                        'benefits': ['Self-paced learning', 'Consistent content', 'Progress tracking'],
                        'challenges': ['Self-motivation required', 'Limited personalization', 'Technical issues']
                    },
                    'blended_learning': {
                        'approach': 'Combination of multiple modalities',
                        'benefits': ['Flexibility', 'Reinforcement', 'Varied learning styles'],
                        'design_principles': ['Seamless integration', 'Progressive complexity', 'Practical application']
                    }
                },
                
                'learning_platforms': {
                    'lms': {
                        'name': 'Learning Management System',
                        'features': ['Course catalog', 'Progress tracking', 'Assessments', 'Reporting', 'Mobile access'],
                        'integrations': ['HRIS', 'Performance management', 'Talent management']
                    },
                    'external_platforms': [
                        {
                            'platform': 'LinkedIn Learning',
                            'content': 'Business and technical skills',
                            'format': 'Video-based courses'
                        },
                        {
                            'platform': 'Coursera for Business',
                            'content': 'University-level courses and specializations',
                            'format': 'Structured learning paths'
                        },
                        {
                            'platform': 'Udemy for Business',
                            'content': 'Practical skills and tools',
                            'format': 'Hands-on projects'
                        }
                    ]
                }
            },
            
            'learning_measurement': {
                'kirkpatrick_model': {
                    'level_1_reaction': {
                        'measures': ['Satisfaction scores', 'Engagement metrics', 'Completion rates'],
                        'methods': ['Post-training surveys', 'Feedback forms', 'Focus groups']
                    },
                    'level_2_learning': {
                        'measures': ['Knowledge acquisition', 'Skill demonstration', 'Attitude change'],
                        'methods': ['Pre/post assessments', 'Practical exercises', 'Simulations']
                    },
                    'level_3_behavior': {
                        'measures': ['On-the-job application', 'Behavior change', 'Performance improvement'],
                        'methods': ['Manager observations', 'Peer feedback', 'Performance metrics']
                    },
                    'level_4_results': {
                        'measures': ['Business impact', 'ROI', 'Organizational outcomes'],
                        'methods': ['Business metrics', 'Cost-benefit analysis', 'Long-term tracking']
                    }
                },
                'key_metrics': {
                    'participation': ['Enrollment rates', 'Completion rates', 'Time to completion'],
                    'effectiveness': ['Assessment scores', 'Skill improvement', 'Certification rates'],
                    'impact': ['Performance improvement', 'Promotion rates', 'Retention rates'],
                    'efficiency': ['Cost per learner', 'Time to competency', 'Resource utilization']
                }
            }
        }
    
    def _load_compliance_policies_data(self) -> Dict[str, Any]:
        """
        Data lengkap tentang compliance dan kebijakan
        """
        return {
            'code_of_conduct': {
                'core_principles': [
                    {
                        'principle': 'Integrity',
                        'description': 'Act honestly and ethically in all business dealings',
                        'examples': [
                            'Provide accurate and complete information',
                            'Avoid conflicts of interest',
                            'Report unethical behavior',
                            'Maintain confidentiality'
                        ]
                    },
                    {
                        'principle': 'Respect',
                        'description': 'Treat all individuals with dignity and respect',
                        'examples': [
                            'Embrace diversity and inclusion',
                            'Prevent harassment and discrimination',
                            'Listen to different perspectives',
                            'Create inclusive environment'
                        ]
                    },
                    {
                        'principle': 'Excellence',
                        'description': 'Strive for excellence in everything we do',
                        'examples': [
                            'Deliver high-quality work',
                            'Continuously improve processes',
                            'Take ownership and accountability',
                            'Exceed customer expectations'
                        ]
                    }
                ],
                'violation_reporting': {
                    'channels': [
                        'Direct supervisor',
                        'HR Business Partner',
                        'Ethics hotline',
                        'Anonymous online portal'
                    ],
                    'protection': 'Non-retaliation policy for good faith reporting',
                    'investigation': 'Prompt and thorough investigation of all reports'
                }
            },
            
            'workplace_policies': {
                'anti_harassment': {
                    'scope': 'All forms of harassment including sexual, racial, and bullying',
                    'definition': 'Unwelcome conduct that creates hostile work environment',
                    'examples': [
                        'Offensive jokes or comments',
                        'Unwanted physical contact',
                        'Discriminatory treatment',
                        'Intimidation or threats'
                    ],
                    'reporting_process': {
                        'immediate_action': 'Report to supervisor or HR immediately',
                        'investigation': 'Confidential investigation within 48 hours',
                        'resolution': 'Appropriate corrective action taken',
                        'follow_up': 'Regular check-ins to ensure no retaliation'
                    }
                },
                
                'equal_opportunity': {
                    'commitment': 'Equal employment opportunity regardless of protected characteristics',
                    'protected_classes': [
                        'Race and ethnicity',
                        'Gender and gender identity',
                        'Sexual orientation',
                        'Religion and beliefs',
                        'Age and disability',
                        'Marital and family status'
                    ],
                    'application_areas': [
                        'Recruitment and hiring',
                        'Compensation and benefits',
                        'Training and development',
                        'Promotion and advancement',
                        'Discipline and termination'
                    ]
                },
                
                'workplace_safety': {
                    'commitment': 'Provide safe and healthy work environment',
                    'responsibilities': {
                        'company': [
                            'Maintain safe facilities and equipment',
                            'Provide safety training and resources',
                            'Investigate and address safety concerns',
                            'Comply with occupational health regulations'
                        ],
                        'employees': [
                            'Follow safety procedures and guidelines',
                            'Report unsafe conditions immediately',
                            'Use personal protective equipment',
                            'Participate in safety training programs'
                        ]
                    },
                    'incident_reporting': {
                        'immediate': 'Report all incidents and near-misses immediately',
                        'documentation': 'Complete incident report within 24 hours',
                        'investigation': 'Root cause analysis and corrective action',
                        'prevention': 'Implement measures to prevent recurrence'
                    }
                },
                
                'data_privacy': {
                    'scope': 'Protection of personal and confidential information',
                    'data_types': [
                        'Employee personal information',
                        'Customer data and records',
                        'Business confidential information',
                        'Intellectual property'
                    ],
                    'handling_principles': [
                        'Collect only necessary information',
                        'Use data only for intended purposes',
                        'Secure data with appropriate controls',
                        'Retain data only as long as needed',
                        'Dispose of data securely'
                    ],
                    'breach_response': {
                        'detection': 'Immediate identification and containment',
                        'assessment': 'Evaluate scope and impact of breach',
                        'notification': 'Notify affected parties and authorities',
                        'remediation': 'Implement corrective measures'
                    }
                }
            },
            
            'employment_policies': {
                'attendance_punctuality': {
                    'work_schedule': {
                        'standard_hours': '40 hours per week, Monday to Friday',
                        'core_hours': '10:00 AM to 3:00 PM (mandatory presence)',
                        'flexible_hours': '7:00 AM to 7:00 PM (flexible start/end)',
                        'break_times': '1 hour lunch break, 15-minute breaks'
                    },
                    'attendance_tracking': {
                        'method': 'Electronic time tracking system',
                        'requirements': 'Clock in/out for all work periods',
                        'exceptions': 'Manager approval for schedule changes'
                    },
                    'tardiness_policy': {
                        'definition': 'Arrival more than 15 minutes after scheduled start',
                        'consequences': [
                            '1st occurrence: Verbal warning',
                            '2nd occurrence: Written warning',
                            '3rd occurrence: Final warning',
                            '4th occurrence: Termination consideration'
                        ]
                    },
                    'absenteeism_policy': {
                        'notification': 'Notify supervisor at least 2 hours before shift',
                        'documentation': 'Medical certificate for sick leave >2 days',
                        'excessive_absence': 'More than 5 unexcused absences in 90 days'
                    }
                },
                
                'leave_policies': {
                    'annual_leave': {
                        'entitlement': '12 days per calendar year',
                        'accrual': 'Earned monthly (1 day per month)',
                        'eligibility': 'After completion of probation period',
                        'application': 'Submit request at least 2 weeks in advance',
                        'approval': 'Subject to manager approval and business needs',
                        'carry_forward': 'Maximum 6 days to following year',
                        'encashment': 'Unused leave can be encashed at year-end'
                    },
                    'sick_leave': {
                        'entitlement': '12 days per calendar year',
                        'usage': 'For personal illness or medical appointments',
                        'notification': 'Inform supervisor as soon as possible',
                        'documentation': 'Medical certificate required for >2 consecutive days',
                        'family_care': 'Can be used for immediate family member care'
                    },
                    'emergency_leave': {
                        'definition': 'Unforeseen circumstances requiring immediate absence',
                        'examples': ['Family emergency', 'Natural disaster', 'Accident'],
                        'notification': 'Contact supervisor within 24 hours',
                        'documentation': 'Supporting evidence may be required',
                        'deduction': 'Deducted from annual leave or unpaid'
                    },
                    'maternity_paternity': {
                        'maternity_leave': {
                            'duration': '3 months (90 calendar days)',
                            'pay': '100% of basic salary',
                            'timing': 'Can start up to 4 weeks before due date',
                            'extension': 'Additional unpaid leave available'
                        },
                        'paternity_leave': {
                            'duration': '2 working days',
                            'pay': '100% of basic salary',
                            'timing': 'Within 30 days of child birth/adoption',
                            'documentation': 'Birth certificate required'
                        }
                    }
                },
                
                'performance_discipline': {
                    'progressive_discipline': {
                        'step_1': {
                            'action': 'Verbal counseling',
                            'documentation': 'Informal note in employee file',
                            'purpose': 'Address minor performance issues'
                        },
                        'step_2': {
                            'action': 'Written warning',
                            'documentation': 'Formal written documentation',
                            'purpose': 'Address continued or serious issues'
                        },
                        'step_3': {
                            'action': 'Final written warning',
                            'documentation': 'Final warning letter',
                            'purpose': 'Last opportunity for improvement'
                        },
                        'step_4': {
                            'action': 'Termination',
                            'documentation': 'Termination letter and final settlement',
                            'purpose': 'End employment relationship'
                        }
                    },
                    'serious_misconduct': {
                        'definition': 'Behavior that may result in immediate termination',
                        'examples': [
                            'Theft or fraud',
                            'Violence or threats',
                            'Substance abuse at work',
                            'Breach of confidentiality',
                            'Insubordination'
                        ],
                        'process': 'Investigation followed by appropriate action'
                    }
                }
            },
            
            'regulatory_compliance': {
                'labor_law': {
                    'minimum_wage': 'Comply with local minimum wage requirements',
                    'overtime': 'Pay overtime for work exceeding 40 hours/week',
                    'record_keeping': 'Maintain accurate employment records',
                    'termination': 'Follow proper termination procedures'
                },
                'tax_compliance': {
                    'income_tax': 'Withhold and remit employee income taxes',
                    'social_security': 'Contribute to social security programs',
                    'reporting': 'Submit required tax reports and filings'
                },
                'health_safety': {
                    'osha_compliance': 'Meet occupational safety standards',
                    'workplace_inspections': 'Conduct regular safety inspections',
                    'training': 'Provide mandatory safety training',
                    'incident_reporting': 'Report workplace injuries and illnesses'
                }
            }
        }
    
    def _load_organizational_structure_data(self) -> Dict[str, Any]:
        """
        Data tentang struktur organisasi
        """
        return {
            'organizational_chart': {
                'executive_level': {
                    'ceo': {
                        'title': 'Chief Executive Officer',
                        'responsibilities': ['Strategic direction', 'Board relations', 'Stakeholder management'],
                        'reports_to': 'Board of Directors'
                    },
                    'direct_reports': [
                        {
                            'title': 'Chief Technology Officer',
                            'department': 'Technology',
                            'team_size': 150
                        },
                        {
                            'title': 'Chief Financial Officer',
                            'department': 'Finance',
                            'team_size': 25
                        },
                        {
                            'title': 'Chief Human Resources Officer',
                            'department': 'Human Resources',
                            'team_size': 20
                        },
                        {
                            'title': 'Chief Marketing Officer',
                            'department': 'Marketing',
                            'team_size': 35
                        },
                        {
                            'title': 'Chief Operations Officer',
                            'department': 'Operations',
                            'team_size': 80
                        }
                    ]
                },
                'department_structure': {
                    'technology': {
                        'teams': [
                            {'name': 'Product Engineering', 'size': 60, 'focus': 'Core product development'},
                            {'name': 'Platform Engineering', 'size': 30, 'focus': 'Infrastructure and platform'},
                            {'name': 'Data Engineering', 'size': 25, 'focus': 'Data pipeline and analytics'},
                            {'name': 'Quality Assurance', 'size': 20, 'focus': 'Testing and quality'},
                            {'name': 'DevOps', 'size': 15, 'focus': 'Deployment and operations'}
                        ]
                    },
                    'human_resources': {
                        'teams': [
                            {'name': 'Talent Acquisition', 'size': 6, 'focus': 'Recruitment and hiring'},
                            {'name': 'HR Business Partners', 'size': 5, 'focus': 'Employee relations and support'},
                            {'name': 'Learning & Development', 'size': 4, 'focus': 'Training and development'},
                            {'name': 'Compensation & Benefits', 'size': 3, 'focus': 'Payroll and benefits'},
                            {'name': 'HR Operations', 'size': 2, 'focus': 'HR processes and systems'}
                        ]
                    }
                }
            },
            'reporting_relationships': {
                'management_levels': {
                    'individual_contributor': {
                        'description': 'Individual contributors without direct reports',
                        'levels': ['Junior', 'Mid-level', 'Senior', 'Principal', 'Distinguished']
                    },
                    'first_line_manager': {
                        'description': 'Managers with individual contributor reports',
                        'typical_span': '5-8 direct reports',
                        'responsibilities': ['Team performance', 'Individual development', 'Operational execution']
                    },
                    'middle_management': {
                        'description': 'Managers of managers',
                        'typical_span': '3-5 direct reports',
                        'responsibilities': ['Strategic planning', 'Resource allocation', 'Cross-team coordination']
                    },
                    'senior_management': {
                        'description': 'Department heads and directors',
                        'typical_span': '2-4 direct reports',
                        'responsibilities': ['Strategic direction', 'Budget management', 'Stakeholder relations']
                    }
                }
            }
        }
    
    def _load_hr_processes_data(self) -> Dict[str, Any]:
        """
        Data tentang proses-proses HR
        """
        return {
            'employee_data_management': {
                'hris_system': {
                    'name': 'Human Resource Information System',
                    'modules': [
                        'Employee master data',
                        'Payroll processing',
                        'Time and attendance',
                        'Performance management',
                        'Learning management',
                        'Recruitment tracking'
                    ],
                    'integrations': ['Payroll system', 'Benefits administration', 'Time tracking']
                },
                'data_categories': {
                    'personal_information': [
                        'Name and contact details',
                        'Emergency contacts',
                        'Identification documents',
                        'Family information'
                    ],
                    'employment_information': [
                        'Job title and department',
                        'Start date and tenure',
                        'Employment status',
                        'Reporting relationships'
                    ],
                    'compensation_information': [
                        'Salary and wage rates',
                        'Benefits enrollment',
                        'Tax withholding information',
                        'Payment methods'
                    ]
                }
            },
            'workflow_automation': {
                'approval_workflows': {
                    'leave_requests': {
                        'steps': ['Employee submission', 'Manager approval', 'HR notification', 'Calendar update'],
                        'sla': '2 business days for approval',
                        'escalation': 'Auto-escalate if no response in 3 days'
                    },
                    'expense_reimbursement': {
                        'steps': ['Employee submission', 'Manager approval', 'Finance review', 'Payment processing'],
                        'sla': '5 business days for processing',
                        'requirements': 'Receipts and business justification'
                    },
                    'training_requests': {
                        'steps': ['Employee request', 'Manager approval', 'Budget check', 'L&D coordination'],
                        'sla': '1 week for approval',
                        'criteria': 'Relevance to role and budget availability'
                    }
                }
            }
        }
    
    def _load_employee_relations_data(self) -> Dict[str, Any]:
        """
        Data tentang hubungan karyawan
        """
        return {
            'employee_engagement': {
                'engagement_surveys': {
                    'frequency': 'Annual comprehensive survey + quarterly pulse surveys',
                    'participation_rate': '85% target',
                    'key_metrics': [
                        'Overall satisfaction',
                        'Manager effectiveness',
                        'Career development',
                        'Work-life balance',
                        'Recognition and rewards'
                    ]
                },
                'engagement_initiatives': [
                    {
                        'initiative': 'Employee Recognition Program',
                        'description': 'Peer-to-peer and manager recognition platform',
                        'frequency': 'Ongoing'
                    },
                    {
                        'initiative': 'Town Hall Meetings',
                        'description': 'Quarterly all-hands meetings with leadership',
                        'frequency': 'Quarterly'
                    },
                    {
                        'initiative': 'Innovation Time',
                        'description': '20% time for personal projects and innovation',
                        'frequency': 'Weekly'
                    }
                ]
            },
            'communication_channels': {
                'formal_channels': [
                    'Company newsletter',
                    'Intranet portal',
                    'Email announcements',
                    'Team meetings',
                    'All-hands meetings'
                ],
                'informal_channels': [
                    'Slack/Teams channels',
                    'Coffee chats',
                    'Lunch and learns',
                    'Social events',
                    'Employee resource groups'
                ]
            }
        }
    
    def search_domain_data(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """
        Mencari data domain berdasarkan query
        """
        results = []
        search_categories = [category] if category else [
            'employee_lifecycle', 'compensation_benefits', 'performance_management',
            'learning_development', 'compliance_policies', 'organizational_structure',
            'hr_processes', 'employee_relations'
        ]
        
        for cat in search_categories:
            if hasattr(self, cat):
                data = getattr(self, cat)
                # Simple text search in data structure
                matches = self._search_in_data(data, query.lower(), cat)
                results.extend(matches)
        
        return results[:10]  # Limit results
    
    def _search_in_data(self, data: Any, query: str, category: str, path: str = "") -> List[Dict[str, Any]]:
        """
        Recursive search in data structure
        """
        results = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                if query in key.lower() or (isinstance(value, str) and query in value.lower()):
                    results.append({
                        'category': category,
                        'path': current_path,
                        'key': key,
                        'value': value,
                        'relevance': self._calculate_relevance(query, key, value)
                    })
                results.extend(self._search_in_data(value, query, category, current_path))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                results.extend(self._search_in_data(item, query, category, current_path))
        elif isinstance(data, str) and query in data.lower():
            results.append({
                'category': category,
                'path': path,
                'content': data,
                'relevance': self._calculate_relevance(query, "", data)
            })
        
        return results
    
    def _calculate_relevance(self, query: str, key: str, value: Any) -> float:
        """
        Calculate relevance score for search results
        """
        score = 0.0
        
        # Exact match in key gets highest score
        if query == key.lower():
            score += 1.0
        elif query in key.lower():
            score += 0.7
        
        # Match in value
        if isinstance(value, str):
            if query == value.lower():
                score += 0.8
            elif query in value.lower():
                score += 0.5
        
        return score
    
    def get_category_overview(self, category: str) -> Dict[str, Any]:
        """
        Mendapatkan overview dari kategori tertentu
        """
        if hasattr(self, category):
            data = getattr(self, category)
            return {
                'category': category,
                'overview': self._generate_overview(data),
                'key_topics': list(data.keys()) if isinstance(data, dict) else [],
                'data_points': self._count_data_points(data)
            }
        return {}
    
    def _generate_overview(self, data: Any) -> str:
        """
        Generate overview text for data category
        """
        if isinstance(data, dict):
            return f"Contains {len(data)} main sections covering various aspects of the topic."
        elif isinstance(data, list):
            return f"Contains {len(data)} items in the collection."
        else:
            return "Single data item."
    
    def _count_data_points(self, data: Any) -> int:
        """
        Count total data points in structure
        """
        if isinstance(data, dict):
            return sum(self._count_data_points(v) for v in data.values())
        elif isinstance(data, list):
            return sum(self._count_data_points(item) for item in data)
        else:
            return 1
    
    def get_detailed_info(self, category: str, topic: str) -> Dict[str, Any]:
        """
        Mendapatkan informasi detail untuk topik tertentu
        """
        if hasattr(self, category):
            data = getattr(self, category)
            if isinstance(data, dict) and topic in data:
                return {
                    'category': category,
                    'topic': topic,
                    'data': data[topic],
                    'related_topics': [k for k in data.keys() if k != topic][:5]
                }
        return {}
    
    def get_process_flow(self, process_name: str) -> Dict[str, Any]:
        """
        Mendapatkan alur proses untuk proses tertentu
        """
        process_flows = {
            'recruitment': self.employee_lifecycle.get('recruitment', {}),
            'onboarding': self.employee_lifecycle.get('onboarding', {}),
            'performance_review': self.performance_management.get('performance_cycle', {}),
            'leave_application': self.hr_processes.get('workflow_automation', {}).get('approval_workflows', {}).get('leave_requests', {})
        }
        
        return process_flows.get(process_name, {})
    
    def get_policy_details(self, policy_area: str) -> Dict[str, Any]:
        """
        Mendapatkan detail kebijakan untuk area tertentu
        """
        if policy_area in ['workplace_policies', 'employment_policies', 'regulatory_compliance']:
            return self.compliance_policies.get(policy_area, {})
        return {}
    
    def get_faq_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Mendapatkan FAQ berdasarkan kategori
        """
        faqs = []
        
        # Extract FAQs from different data sources
        if category == 'recruitment':
            recruitment_data = self.employee_lifecycle.get('recruitment', {})
            faqs.extend(recruitment_data.get('common_questions', []))
        
        elif category == 'benefits':
            benefits_data = self.compensation_benefits.get('benefits_package', {})
            # Generate FAQs from benefits data
            for benefit_type, details in benefits_data.items():
                if isinstance(details, dict):
                    faqs.append({
                        'question': f'Apa saja {benefit_type} yang tersedia?',
                        'answer': f'Tersedia berbagai {benefit_type} termasuk komponen-komponen yang telah ditetapkan perusahaan.',
                        'details': str(details)[:200] + '...' if len(str(details)) > 200 else str(details)
                    })
        
        elif category == 'performance':
            performance_data = self.performance_management.get('performance_ratings', {})
            faqs.append({
                'question': 'Bagaimana sistem penilaian kinerja bekerja?',
                'answer': 'Sistem penilaian menggunakan skala 1-5 dengan distribusi yang telah ditetapkan.',
                'details': 'Penilaian dilakukan secara berkala dengan proses kalibrasi untuk memastikan konsistensi.'
            })
        
        return faqs
    
    def export_data(self, format_type: str = 'json') -> str:
        """
        Export all domain data in specified format
        """
        all_data = {
            'employee_lifecycle': self.employee_lifecycle,
            'compensation_benefits': self.compensation_benefits,
            'performance_management': self.performance_management,
            'learning_development': self.learning_development,
            'compliance_policies': self.compliance_policies,
            'organizational_structure': self.organizational_structure,
            'hr_processes': self.hr_processes,
            'employee_relations': self.employee_relations
        }
        
        if format_type == 'json':
            return json.dumps(all_data, indent=2, ensure_ascii=False)
        else:
            return str(all_data)