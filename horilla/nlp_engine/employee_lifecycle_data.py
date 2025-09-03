# -*- coding: utf-8 -*-
"""
Employee Lifecycle Data
Berisi informasi lengkap tentang siklus hidup karyawan dari recruitment hingga exit
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class EmployeeLifecycleData:
    """
    Kelas untuk mengelola data siklus hidup karyawan
    """
    
    def __init__(self):
        self.recruitment_process = self._load_recruitment_process()
        self.onboarding_process = self._load_onboarding_process()
        self.performance_management = self._load_performance_management()
        self.career_development = self._load_career_development()
        self.employee_engagement = self._load_employee_engagement()
        self.retention_strategies = self._load_retention_strategies()
        self.offboarding_process = self._load_offboarding_process()
        self.alumni_relations = self._load_alumni_relations()
    
    def _load_recruitment_process(self) -> Dict[str, Any]:
        """
        Data tentang proses recruitment
        """
        return {
            'recruitment_stages': {
                'job_analysis': {
                    'description': 'Analisis kebutuhan posisi dan kualifikasi',
                    'activities': [
                        'Review job description dan requirements',
                        'Analisis competency yang dibutuhkan',
                        'Tentukan budget dan timeline recruitment',
                        'Identifikasi sumber kandidat potensial'
                    ],
                    'deliverables': [
                        'Job description yang updated',
                        'Person specification',
                        'Recruitment plan dan timeline',
                        'Budget approval'
                    ],
                    'duration': '1-2 minggu'
                },
                'sourcing': {
                    'description': 'Pencarian dan identifikasi kandidat potensial',
                    'channels': [
                        {
                            'channel': 'Internal Recruitment',
                            'methods': ['Job posting internal', 'Employee referral', 'Talent pool internal'],
                            'advantages': ['Cost effective', 'Faster onboarding', 'Employee motivation'],
                            'considerations': ['Limited talent pool', 'Potential internal conflicts']
                        },
                        {
                            'channel': 'External Job Boards',
                            'methods': ['JobStreet', 'LinkedIn', 'Indeed', 'Glassdoor'],
                            'advantages': ['Wide reach', 'Diverse candidates', 'Cost effective'],
                            'considerations': ['High volume applications', 'Quality screening needed']
                        },
                        {
                            'channel': 'Professional Networks',
                            'methods': ['LinkedIn recruiting', 'Industry associations', 'Alumni networks'],
                            'advantages': ['Quality candidates', 'Passive candidates', 'Industry expertise'],
                            'considerations': ['Time intensive', 'Relationship building required']
                        },
                        {
                            'channel': 'Recruitment Agencies',
                            'methods': ['Executive search', 'Contingency recruitment', 'RPO services'],
                            'advantages': ['Specialized expertise', 'Time saving', 'Guaranteed results'],
                            'considerations': ['Higher cost', 'Less control over process']
                        }
                    ],
                    'duration': '2-4 minggu'
                },
                'screening': {
                    'description': 'Penyaringan awal kandidat berdasarkan kriteria',
                    'screening_methods': [
                        {
                            'method': 'Resume/CV Screening',
                            'criteria': ['Education background', 'Work experience', 'Skills match', 'Career progression'],
                            'tools': ['ATS systems', 'AI screening tools', 'Manual review'],
                            'duration': '1-2 hari per batch'
                        },
                        {
                            'method': 'Phone/Video Screening',
                            'purpose': 'Initial conversation dan basic qualification check',
                            'duration': '15-30 menit per kandidat',
                            'key_areas': ['Communication skills', 'Interest level', 'Salary expectations', 'Availability']
                        },
                        {
                            'method': 'Online Assessments',
                            'types': ['Cognitive ability tests', 'Personality assessments', 'Skills tests', 'Situational judgment'],
                            'benefits': ['Objective evaluation', 'Predictive validity', 'Efficient screening'],
                            'considerations': ['Test validity', 'Candidate experience', 'Legal compliance']
                        }
                    ],
                    'duration': '1-2 minggu'
                },
                'interviewing': {
                    'description': 'Proses wawancara mendalam dengan kandidat terpilih',
                    'interview_types': [
                        {
                            'type': 'Structured Interview',
                            'description': 'Wawancara dengan pertanyaan standar untuk semua kandidat',
                            'advantages': ['Consistency', 'Legal compliance', 'Objective comparison'],
                            'best_practices': [
                                'Develop standardized questions',
                                'Use behavioral interview techniques',
                                'Score responses consistently',
                                'Document all responses'
                            ]
                        },
                        {
                            'type': 'Panel Interview',
                            'description': 'Wawancara dengan multiple interviewers',
                            'participants': ['Hiring manager', 'HR representative', 'Team members', 'Senior leadership'],
                            'benefits': ['Multiple perspectives', 'Reduced bias', 'Team buy-in'],
                            'coordination_tips': [
                                'Assign specific areas to each panelist',
                                'Brief all panelists beforehand',
                                'Designate lead interviewer',
                                'Debrief immediately after'
                            ]
                        },
                        {
                            'type': 'Technical Interview',
                            'description': 'Assessment kemampuan teknis spesifik',
                            'methods': ['Coding challenges', 'Case studies', 'Practical demonstrations', 'Portfolio reviews'],
                            'evaluation_criteria': ['Technical competency', 'Problem-solving approach', 'Code quality', 'Communication of technical concepts']
                        },
                        {
                            'type': 'Cultural Fit Interview',
                            'description': 'Assessment kesesuaian dengan budaya perusahaan',
                            'focus_areas': ['Values alignment', 'Work style preferences', 'Team collaboration', 'Adaptability'],
                            'techniques': ['Scenario-based questions', 'Values-based discussions', 'Team interaction sessions']
                        }
                    ],
                    'duration': '2-3 minggu'
                },
                'selection': {
                    'description': 'Proses pemilihan kandidat final',
                    'decision_factors': [
                        {
                            'factor': 'Technical Competency',
                            'weight': '40%',
                            'assessment_methods': ['Technical interviews', 'Skills assessments', 'Work samples']
                        },
                        {
                            'factor': 'Cultural Fit',
                            'weight': '25%',
                            'assessment_methods': ['Behavioral interviews', 'Team interactions', 'Values assessment']
                        },
                        {
                            'factor': 'Experience and Background',
                            'weight': '20%',
                            'assessment_methods': ['Resume review', 'Reference checks', 'Portfolio evaluation']
                        },
                        {
                            'factor': 'Growth Potential',
                            'weight': '15%',
                            'assessment_methods': ['Career discussions', 'Learning agility assessment', 'Leadership potential']
                        }
                    ],
                    'reference_checks': {
                        'types': ['Professional references', 'Academic references', 'Character references'],
                        'key_questions': [
                            'Quality of work performance',
                            'Reliability and attendance',
                            'Teamwork and collaboration',
                            'Areas for improvement',
                            'Eligibility for rehire'
                        ],
                        'best_practices': [
                            'Get candidate consent',
                            'Use structured reference forms',
                            'Document all conversations',
                            'Verify reference authenticity'
                        ]
                    },
                    'duration': '1 minggu'
                },
                'offer_negotiation': {
                    'description': 'Proses penawaran dan negosiasi terms of employment',
                    'offer_components': [
                        {
                            'component': 'Base Salary',
                            'considerations': ['Market benchmarks', 'Internal equity', 'Budget constraints', 'Candidate expectations']
                        },
                        {
                            'component': 'Benefits Package',
                            'elements': ['Health insurance', 'Retirement plans', 'Paid time off', 'Professional development']
                        },
                        {
                            'component': 'Work Arrangements',
                            'options': ['Remote work', 'Flexible hours', 'Hybrid schedule', 'Travel requirements']
                        },
                        {
                            'component': 'Career Development',
                            'offerings': ['Training opportunities', 'Mentorship programs', 'Career pathing', 'Tuition reimbursement']
                        }
                    ],
                    'negotiation_strategies': [
                        'Understand candidate priorities',
                        'Present total compensation value',
                        'Be transparent about constraints',
                        'Focus on win-win solutions',
                        'Document all agreements'
                    ],
                    'duration': '3-5 hari'
                }
            },
            
            'recruitment_metrics': {
                'efficiency_metrics': [
                    {
                        'metric': 'Time to Fill',
                        'definition': 'Days from job posting to offer acceptance',
                        'benchmark': '30-45 days for most positions',
                        'improvement_strategies': ['Streamline approval processes', 'Improve sourcing channels', 'Enhance interview scheduling']
                    },
                    {
                        'metric': 'Cost per Hire',
                        'definition': 'Total recruitment costs divided by number of hires',
                        'components': ['Advertising costs', 'Agency fees', 'Internal time costs', 'Assessment tools'],
                        'benchmark': 'Varies by industry and position level'
                    },
                    {
                        'metric': 'Source Effectiveness',
                        'definition': 'Quality and quantity of candidates by source',
                        'measurement': ['Applications per source', 'Interview rate', 'Hire rate', 'Retention rate'],
                        'optimization': 'Focus resources on most effective sources'
                    }
                ],
                'quality_metrics': [
                    {
                        'metric': 'Quality of Hire',
                        'definition': 'Performance and retention of new hires',
                        'measurement': ['90-day performance ratings', '1-year retention rate', 'Manager satisfaction'],
                        'improvement_focus': 'Better assessment methods and cultural fit evaluation'
                    },
                    {
                        'metric': 'Candidate Experience',
                        'definition': 'Candidate satisfaction with recruitment process',
                        'measurement': ['Survey feedback', 'Process completion rates', 'Offer acceptance rates'],
                        'impact': 'Affects employer brand and future applications'
                    }
                ]
            }
        }
    
    def _load_onboarding_process(self) -> Dict[str, Any]:
        """
        Data tentang proses onboarding
        """
        return {
            'pre_boarding': {
                'description': 'Aktivitas sebelum hari pertama kerja',
                'timeline': '1-2 minggu sebelum start date',
                'activities': [
                    {
                        'activity': 'Welcome Communication',
                        'details': [
                            'Send welcome email dengan informasi penting',
                            'Share company handbook dan policies',
                            'Provide first day logistics (time, location, dress code)',
                            'Introduce buddy/mentor system'
                        ]
                    },
                    {
                        'activity': 'Administrative Setup',
                        'details': [
                            'Prepare workspace dan equipment',
                            'Setup IT accounts dan access',
                            'Order business cards dan name plates',
                            'Complete background checks dan documentation'
                        ]
                    },
                    {
                        'activity': 'Team Preparation',
                        'details': [
                            'Inform team about new hire',
                            'Plan welcome activities',
                            'Assign initial projects dan tasks',
                            'Schedule meet-and-greet sessions'
                        ]
                    }
                ]
            },
            
            'first_day': {
                'description': 'Aktivitas hari pertama kerja',
                'objectives': [
                    'Make positive first impression',
                    'Complete essential paperwork',
                    'Begin cultural integration',
                    'Set clear expectations'
                ],
                'schedule_template': {
                    '09:00-09:30': {
                        'activity': 'Welcome dan Check-in',
                        'participants': ['HR representative', 'Direct manager'],
                        'deliverables': ['Welcome packet', 'ID badge', 'Keys/access cards']
                    },
                    '09:30-10:30': {
                        'activity': 'HR Orientation',
                        'topics': ['Company overview', 'Policies dan procedures', 'Benefits enrollment', 'Compliance training'],
                        'materials': ['Employee handbook', 'Benefits guide', 'Compliance certificates']
                    },
                    '10:30-11:00': {
                        'activity': 'IT Setup',
                        'tasks': ['Computer setup', 'Software installation', 'Account activation', 'Security briefing'],
                        'support': 'IT technician'
                    },
                    '11:00-12:00': {
                        'activity': 'Department Introduction',
                        'participants': ['Direct manager', 'Team members'],
                        'focus': ['Team dynamics', 'Current projects', 'Communication protocols']
                    },
                    '12:00-13:00': {
                        'activity': 'Lunch dengan Team',
                        'purpose': 'Informal relationship building',
                        'participants': 'Immediate team members'
                    },
                    '13:00-14:00': {
                        'activity': 'Workspace Setup',
                        'tasks': ['Desk organization', 'Equipment familiarization', 'Personalization'],
                        'support': 'Assigned buddy'
                    },
                    '14:00-15:30': {
                        'activity': 'Role-Specific Training',
                        'content': ['Job responsibilities', 'Performance expectations', 'Initial assignments'],
                        'facilitator': 'Direct manager'
                    },
                    '15:30-16:00': {
                        'activity': 'Company Tour',
                        'locations': ['Different departments', 'Common areas', 'Emergency exits', 'Facilities'],
                        'guide': 'HR representative atau buddy'
                    },
                    '16:00-17:00': {
                        'activity': 'First Day Wrap-up',
                        'tasks': ['Q&A session', 'Schedule follow-up meetings', 'Feedback collection'],
                        'participants': ['HR', 'Direct manager']
                    }
                }
            },
            
            'first_week': {
                'description': 'Aktivitas minggu pertama',
                'objectives': [
                    'Complete essential training',
                    'Build relationships',
                    'Understand company culture',
                    'Begin productive work'
                ],
                'daily_activities': {
                    'day_2': [
                        'Deep dive into role responsibilities',
                        'Meet key stakeholders',
                        'Begin skills assessment',
                        'Start initial projects'
                    ],
                    'day_3': [
                        'Product/service training',
                        'Customer/client overview',
                        'Process documentation review',
                        'Shadow experienced team member'
                    ],
                    'day_4': [
                        'Systems dan tools training',
                        'Compliance training completion',
                        'Goal setting session',
                        'Feedback check-in'
                    ],
                    'day_5': [
                        'Week 1 review meeting',
                        'Address questions dan concerns',
                        'Plan for week 2',
                        'Social integration activities'
                    ]
                }
            },
            
            'first_month': {
                'description': 'Aktivitas bulan pertama',
                'milestones': [
                    {
                        'week': 2,
                        'focus': 'Skill Development',
                        'activities': [
                            'Complete role-specific training modules',
                            'Begin independent work assignments',
                            'Establish regular check-in schedule',
                            'Join relevant meetings dan projects'
                        ]
                    },
                    {
                        'week': 3,
                        'focus': 'Integration dan Performance',
                        'activities': [
                            'Take on increased responsibilities',
                            'Participate in team initiatives',
                            'Receive performance feedback',
                            'Identify development needs'
                        ]
                    },
                    {
                        'week': 4,
                        'focus': 'Evaluation dan Planning',
                        'activities': [
                            'Complete 30-day review',
                            'Set 90-day goals',
                            'Assess onboarding effectiveness',
                            'Plan continued development'
                        ]
                    }
                ]
            },
            
            'onboarding_best_practices': {
                'personalization': [
                    'Tailor onboarding to role dan experience level',
                    'Consider individual learning styles',
                    'Accommodate special needs atau preferences',
                    'Adjust pace based on progress'
                ],
                'engagement_strategies': [
                    'Assign dedicated buddy atau mentor',
                    'Create opportunities for social interaction',
                    'Involve new hire in meaningful projects early',
                    'Celebrate milestones dan achievements'
                ],
                'feedback_mechanisms': [
                    'Regular check-ins dengan manager',
                    'Pulse surveys at key intervals',
                    'Open door policy for questions',
                    'Exit interviews for early departures'
                ],
                'technology_integration': [
                    'Use onboarding platforms dan apps',
                    'Provide self-service resources',
                    'Enable mobile access to information',
                    'Integrate dengan HRIS systems'
                ]
            }
        }
    
    def _load_performance_management(self) -> Dict[str, Any]:
        """
        Data tentang performance management
        """
        return {
            'performance_cycle': {
                'annual_cycle': {
                    'q1': {
                        'focus': 'Goal Setting dan Planning',
                        'activities': [
                            'Set annual performance goals',
                            'Align individual goals dengan company objectives',
                            'Create development plans',
                            'Establish success metrics'
                        ],
                        'deliverables': ['Performance goals document', 'Development plan', 'Success metrics']
                    },
                    'q2': {
                        'focus': 'Mid-Year Review',
                        'activities': [
                            'Assess progress towards goals',
                            'Provide feedback dan coaching',
                            'Adjust goals if necessary',
                            'Identify support needs'
                        ],
                        'deliverables': ['Mid-year review document', 'Updated goals', 'Development progress report']
                    },
                    'q3': {
                        'focus': 'Performance Monitoring',
                        'activities': [
                            'Continue regular check-ins',
                            'Monitor performance metrics',
                            'Provide ongoing feedback',
                            'Address performance issues'
                        ],
                        'deliverables': ['Performance tracking reports', 'Feedback documentation']
                    },
                    'q4': {
                        'focus': 'Annual Review dan Planning',
                        'activities': [
                            'Complete annual performance review',
                            'Assess goal achievement',
                            'Plan for next year',
                            'Make compensation decisions'
                        ],
                        'deliverables': ['Annual review document', 'Rating dan ranking', 'Next year goals']
                    }
                }
            },
            
            'performance_frameworks': {
                'okr_framework': {
                    'description': 'Objectives and Key Results',
                    'structure': {
                        'objectives': {
                            'definition': 'Qualitative, inspirational descriptions of what you want to achieve',
                            'characteristics': ['Significant', 'Concrete', 'Action-oriented', 'Inspirational'],
                            'examples': [
                                'Improve customer satisfaction',
                                'Enhance product quality',
                                'Increase market share'
                            ]
                        },
                        'key_results': {
                            'definition': 'Quantitative measures that track achievement of objectives',
                            'characteristics': ['Specific', 'Measurable', 'Achievable', 'Time-bound'],
                            'examples': [
                                'Increase NPS score from 7 to 8.5',
                                'Reduce defect rate to less than 1%',
                                'Achieve 15% market share in target segment'
                            ]
                        }
                    },
                    'best_practices': [
                        'Set 3-5 objectives per person/team',
                        'Each objective should have 2-4 key results',
                        'Make goals ambitious but achievable',
                        'Review dan update quarterly',
                        'Ensure alignment across organization'
                    ]
                },
                'smart_goals': {
                    'description': 'Specific, Measurable, Achievable, Relevant, Time-bound goals',
                    'components': {
                        'specific': 'Clearly defined dan unambiguous',
                        'measurable': 'Quantifiable dan trackable',
                        'achievable': 'Realistic dan attainable',
                        'relevant': 'Aligned dengan broader objectives',
                        'time_bound': 'Has clear deadline atau timeframe'
                    },
                    'examples': [
                        {
                            'goal': 'Increase sales revenue by 20% in Q4 2024',
                            'breakdown': {
                                'specific': 'Increase sales revenue',
                                'measurable': '20% increase',
                                'achievable': 'Based on market analysis dan resources',
                                'relevant': 'Supports company growth objectives',
                                'time_bound': 'By end of Q4 2024'
                            }
                        }
                    ]
                },
                'competency_based': {
                    'description': 'Performance evaluation based on core competencies',
                    'competency_categories': [
                        {
                            'category': 'Technical Competencies',
                            'description': 'Job-specific skills dan knowledge',
                            'examples': ['Programming languages', 'Financial analysis', 'Project management']
                        },
                        {
                            'category': 'Behavioral Competencies',
                            'description': 'How work is performed',
                            'examples': ['Communication', 'Teamwork', 'Problem-solving', 'Leadership']
                        },
                        {
                            'category': 'Cultural Competencies',
                            'description': 'Alignment dengan company values',
                            'examples': ['Innovation', 'Customer focus', 'Integrity', 'Collaboration']
                        }
                    ],
                    'rating_scales': [
                        {
                            'scale': '5-Point Scale',
                            'levels': {
                                '5': 'Exceptional - Consistently exceeds expectations',
                                '4': 'Exceeds - Regularly surpasses expectations',
                                '3': 'Meets - Consistently meets expectations',
                                '2': 'Below - Sometimes meets expectations',
                                '1': 'Unsatisfactory - Rarely meets expectations'
                            }
                        }
                    ]
                }
            },
            
            'feedback_culture': {
                'continuous_feedback': {
                    'principles': [
                        'Feedback should be timely dan specific',
                        'Focus on behavior dan impact, not personality',
                        'Provide both positive dan constructive feedback',
                        'Create safe environment for open dialogue'
                    ],
                    'feedback_types': [
                        {
                            'type': 'Real-time Feedback',
                            'timing': 'Immediately after observed behavior',
                            'purpose': 'Reinforce good performance atau correct issues quickly',
                            'format': 'Brief, informal conversation'
                        },
                        {
                            'type': 'Regular Check-ins',
                            'timing': 'Weekly atau bi-weekly meetings',
                            'purpose': 'Ongoing performance discussion dan support',
                            'format': 'Structured one-on-one meetings'
                        },
                        {
                            'type': 'Project Reviews',
                            'timing': 'At project milestones atau completion',
                            'purpose': 'Assess project performance dan lessons learned',
                            'format': 'Formal review meeting dengan documentation'
                        }
                    ]
                },
                '360_degree_feedback': {
                    'description': 'Multi-source feedback from various stakeholders',
                    'participants': [
                        {
                            'source': 'Direct Manager',
                            'perspective': 'Performance against goals dan expectations',
                            'focus_areas': ['Goal achievement', 'Skill development', 'Behavior observation']
                        },
                        {
                            'source': 'Peers/Colleagues',
                            'perspective': 'Collaboration dan teamwork',
                            'focus_areas': ['Communication', 'Cooperation', 'Reliability', 'Support']
                        },
                        {
                            'source': 'Direct Reports',
                            'perspective': 'Leadership dan management effectiveness',
                            'focus_areas': ['Leadership style', 'Communication', 'Support', 'Development']
                        },
                        {
                            'source': 'Internal Customers',
                            'perspective': 'Service quality dan responsiveness',
                            'focus_areas': ['Service delivery', 'Responsiveness', 'Quality', 'Professionalism']
                        },
                        {
                            'source': 'Self-Assessment',
                            'perspective': 'Self-awareness dan reflection',
                            'focus_areas': ['Strengths', 'Development areas', 'Goals', 'Aspirations']
                        }
                    ],
                    'implementation_steps': [
                        'Define purpose dan scope',
                        'Select participants dan reviewers',
                        'Design feedback questionnaire',
                        'Collect feedback anonymously',
                        'Compile dan analyze results',
                        'Facilitate feedback discussion',
                        'Create development action plan'
                    ]
                }
            }
        }
    
    def _load_career_development(self) -> Dict[str, Any]:
        """
        Data tentang career development
        """
        return {
            'career_pathing': {
                'career_frameworks': [
                    {
                        'framework': 'Dual Career Ladder',
                        'description': 'Separate advancement paths for technical dan managerial roles',
                        'paths': {
                            'technical_track': {
                                'levels': ['Junior', 'Mid-level', 'Senior', 'Principal', 'Distinguished'],
                                'focus': 'Deep technical expertise dan innovation',
                                'progression_criteria': ['Technical skills', 'Problem-solving', 'Innovation', 'Mentoring']
                            },
                            'management_track': {
                                'levels': ['Team Lead', 'Manager', 'Senior Manager', 'Director', 'VP'],
                                'focus': 'People leadership dan business management',
                                'progression_criteria': ['Leadership skills', 'Business acumen', 'Team development', 'Results delivery']
                            }
                        }
                    },
                    {
                        'framework': 'Competency-Based Progression',
                        'description': 'Advancement based on demonstrated competencies',
                        'competency_levels': {
                            'developing': 'Learning dan applying basic skills',
                            'proficient': 'Consistently demonstrates competency',
                            'advanced': 'Exceeds expectations dan helps others',
                            'expert': 'Recognized authority dan thought leader'
                        }
                    }
                ],
                'career_planning_process': {
                    'self_assessment': {
                        'tools': [
                            'Skills inventory',
                            'Interest assessments',
                            'Values clarification',
                            'Personality assessments'
                        ],
                        'outcomes': [
                            'Understanding of strengths dan development areas',
                            'Clarity on career interests dan values',
                            'Identification of potential career paths'
                        ]
                    },
                    'goal_setting': {
                        'timeframes': {
                            'short_term': '1-2 years - Immediate skill development dan role enhancement',
                            'medium_term': '3-5 years - Career advancement atau transition',
                            'long_term': '5+ years - Senior leadership atau specialized expertise'
                        },
                        'goal_categories': [
                            'Skill development goals',
                            'Experience acquisition goals',
                            'Network building goals',
                            'Position advancement goals'
                        ]
                    },
                    'development_planning': {
                        'development_methods': [
                            {
                                'method': 'Formal Training',
                                'examples': ['Workshops', 'Courses', 'Certifications', 'Conferences'],
                                'benefits': 'Structured learning dan credentials'
                            },
                            {
                                'method': 'On-the-Job Learning',
                                'examples': ['Stretch assignments', 'Job rotation', 'Cross-training', 'Special projects'],
                                'benefits': 'Practical experience dan skill application'
                            },
                            {
                                'method': 'Mentoring dan Coaching',
                                'examples': ['Formal mentoring programs', 'Executive coaching', 'Peer mentoring'],
                                'benefits': 'Personalized guidance dan support'
                            },
                            {
                                'method': 'Self-Directed Learning',
                                'examples': ['Reading', 'Online courses', 'Professional associations', 'Research'],
                                'benefits': 'Flexible dan self-paced learning'
                            }
                        ]
                    }
                }
            },
            
            'succession_planning': {
                'key_positions': {
                    'identification_criteria': [
                        'Critical to business operations',
                        'Difficult to replace externally',
                        'High impact on organizational performance',
                        'Specialized knowledge atau skills required'
                    ],
                    'succession_readiness_levels': {
                        'ready_now': 'Can assume role immediately dengan minimal transition',
                        'ready_1_2_years': 'Will be ready dengan targeted development',
                        'ready_2_3_years': 'Has potential but needs significant development',
                        'longer_term': 'Early career high potential'
                    }
                },
                'talent_pools': {
                    'high_potential_identification': {
                        'criteria': [
                            'Consistent high performance',
                            'Leadership capability',
                            'Learning agility',
                            'Cultural fit',
                            'Aspiration for advancement'
                        ],
                        'assessment_methods': [
                            'Performance reviews',
                            'Leadership assessments',
                            'Talent review discussions',
                            '360-degree feedback',
                            'Assessment centers'
                        ]
                    },
                    'development_programs': [
                        {
                            'program': 'Leadership Development Program',
                            'target': 'High-potential managers',
                            'duration': '12-18 months',
                            'components': ['Leadership training', 'Executive coaching', 'Stretch assignments', 'Mentoring']
                        },
                        {
                            'program': 'Emerging Leaders Program',
                            'target': 'Early-career high potentials',
                            'duration': '6-12 months',
                            'components': ['Leadership fundamentals', 'Cross-functional exposure', 'Project leadership']
                        }
                    ]
                }
            },
            
            'learning_development': {
                'learning_culture': {
                    'principles': [
                        'Continuous learning is everyone\'s responsibility',
                        'Learning from failures is encouraged',
                        'Knowledge sharing is valued dan rewarded',
                        'Innovation requires experimentation dan learning'
                    ],
                    'supporting_practices': [
                        'Dedicated learning time (e.g., 20% time)',
                        'Learning dan development budgets',
                        'Internal knowledge sharing sessions',
                        'Recognition for learning achievements'
                    ]
                },
                'learning_technologies': {
                    'learning_management_systems': {
                        'features': [
                            'Course catalog dan enrollment',
                            'Progress tracking dan reporting',
                            'Assessments dan certifications',
                            'Social learning features'
                        ],
                        'benefits': [
                            'Centralized learning resources',
                            'Personalized learning paths',
                            'Analytics dan insights',
                            'Cost-effective delivery'
                        ]
                    },
                    'microlearning': {
                        'characteristics': [
                            'Short, focused learning modules',
                            'Just-in-time delivery',
                            'Mobile-friendly format',
                            'Bite-sized content'
                        ],
                        'applications': [
                            'Skill refreshers',
                            'Compliance training',
                            'Product updates',
                            'Process reminders'
                        ]
                    }
                }
            }
        }
    
    def _load_employee_engagement(self) -> Dict[str, Any]:
        """
        Data tentang employee engagement
        """
        return {
            'engagement_drivers': {
                'intrinsic_motivators': [
                    {
                        'driver': 'Purpose dan Meaning',
                        'description': 'Connection to organizational mission dan personal values',
                        'strategies': [
                            'Communicate company purpose clearly',
                            'Connect individual roles to larger impact',
                            'Encourage volunteer dan community involvement',
                            'Share success stories dan customer impact'
                        ]
                    },
                    {
                        'driver': 'Autonomy dan Control',
                        'description': 'Freedom to make decisions dan control work methods',
                        'strategies': [
                            'Delegate decision-making authority',
                            'Provide flexible work arrangements',
                            'Encourage innovation dan experimentation',
                            'Minimize micromanagement'
                        ]
                    },
                    {
                        'driver': 'Mastery dan Growth',
                        'description': 'Opportunities to develop skills dan expertise',
                        'strategies': [
                            'Provide challenging assignments',
                            'Offer learning dan development opportunities',
                            'Create clear career progression paths',
                            'Encourage skill diversification'
                        ]
                    }
                ],
                'extrinsic_motivators': [
                    {
                        'driver': 'Recognition dan Rewards',
                        'description': 'Acknowledgment of contributions dan achievements',
                        'strategies': [
                            'Implement peer recognition programs',
                            'Celebrate achievements publicly',
                            'Provide meaningful rewards',
                            'Offer advancement opportunities'
                        ]
                    },
                    {
                        'driver': 'Compensation dan Benefits',
                        'description': 'Fair dan competitive total rewards',
                        'strategies': [
                            'Conduct regular market analysis',
                            'Ensure internal pay equity',
                            'Offer comprehensive benefits',
                            'Provide performance-based incentives'
                        ]
                    }
                ]
            },
            
            'engagement_measurement': {
                'survey_methods': [
                    {
                        'method': 'Annual Engagement Survey',
                        'frequency': 'Once per year',
                        'scope': 'Comprehensive engagement assessment',
                        'sample_questions': [
                            'I would recommend this company as a great place to work',
                            'I have the resources dan support to do my job effectively',
                            'My manager cares about me as a person',
                            'I see a clear path for career advancement'
                        ]
                    },
                    {
                        'method': 'Pulse Surveys',
                        'frequency': 'Quarterly atau monthly',
                        'scope': 'Quick check on key engagement indicators',
                        'benefits': [
                            'More frequent feedback',
                            'Ability to track trends',
                            'Lower survey fatigue',
                            'Faster response to issues'
                        ]
                    },
                    {
                        'method': 'Stay Interviews',
                        'frequency': 'As needed',
                        'scope': 'One-on-one conversations dengan high performers',
                        'purpose': 'Understand what keeps employees engaged dan identify retention risks'
                    }
                ],
                'engagement_metrics': [
                    {
                        'metric': 'Employee Net Promoter Score (eNPS)',
                        'calculation': '% Promoters - % Detractors',
                        'interpretation': {
                            'above_50': 'Excellent engagement',
                            '10_to_50': 'Good engagement',
                            '0_to_10': 'Moderate engagement',
                            'below_0': 'Poor engagement'
                        }
                    },
                    {
                        'metric': 'Engagement Index',
                        'components': ['Say (advocacy)', 'Stay (retention intent)', 'Strive (discretionary effort)'],
                        'calculation': 'Average score across engagement dimensions'
                    }
                ]
            },
            
            'engagement_initiatives': {
                'recognition_programs': [
                    {
                        'program': 'Peer-to-Peer Recognition',
                        'description': 'Platform for employees to recognize each other',
                        'features': ['Digital recognition platform', 'Points-based rewards', 'Social sharing', 'Manager visibility']
                    },
                    {
                        'program': 'Service Awards',
                        'description': 'Recognition for years of service',
                        'milestones': ['1 year', '5 years', '10 years', '15 years', '20+ years'],
                        'rewards': ['Certificates', 'Gifts', 'Extra PTO', 'Special experiences']
                    },
                    {
                        'program': 'Achievement Awards',
                        'description': 'Recognition for exceptional performance atau contributions',
                        'categories': ['Innovation', 'Customer service', 'Teamwork', 'Leadership'],
                        'selection_process': 'Nomination-based dengan review committee'
                    }
                ],
                'wellness_programs': [
                    {
                        'program': 'Physical Wellness',
                        'components': ['Gym memberships', 'Fitness challenges', 'Health screenings', 'Ergonomic assessments'],
                        'benefits': 'Improved health, reduced healthcare costs, increased energy'
                    },
                    {
                        'program': 'Mental Health Support',
                        'components': ['Employee assistance programs', 'Stress management workshops', 'Mental health days', 'Counseling services'],
                        'benefits': 'Reduced stress, improved resilience, better work-life balance'
                    },
                    {
                        'program': 'Financial Wellness',
                        'components': ['Financial planning workshops', 'Retirement planning', 'Emergency savings programs', 'Financial counseling'],
                        'benefits': 'Reduced financial stress, improved financial security'
                    }
                ],
                'work_life_balance': [
                    {
                        'initiative': 'Flexible Work Arrangements',
                        'options': ['Remote work', 'Hybrid schedules', 'Flexible hours', 'Compressed workweeks'],
                        'implementation': 'Policy framework dengan manager approval'
                    },
                    {
                        'initiative': 'Time Off Policies',
                        'components': ['Generous PTO', 'Sabbatical programs', 'Mental health days', 'Volunteer time off'],
                        'philosophy': 'Encourage employees to recharge dan pursue personal interests'
                    }
                ]
            }
        }
    
    def _load_retention_strategies(self) -> Dict[str, Any]:
        """
        Data tentang strategi retention
        """
        return {
            'retention_factors': {
                'top_retention_drivers': [
                    {
                        'factor': 'Career Development Opportunities',
                        'importance': 'High',
                        'strategies': [
                            'Create clear career paths',
                            'Provide skill development opportunities',
                            'Offer internal mobility',
                            'Support external education'
                        ]
                    },
                    {
                        'factor': 'Manager Relationship',
                        'importance': 'High',
                        'strategies': [
                            'Train managers in people leadership',
                            'Provide regular feedback dan coaching',
                            'Ensure manager-employee fit',
                            'Address manager performance issues'
                        ]
                    },
                    {
                        'factor': 'Work-Life Balance',
                        'importance': 'High',
                        'strategies': [
                            'Offer flexible work arrangements',
                            'Respect personal time boundaries',
                            'Provide adequate time off',
                            'Support family responsibilities'
                        ]
                    },
                    {
                        'factor': 'Compensation dan Benefits',
                        'importance': 'Medium-High',
                        'strategies': [
                            'Conduct regular market analysis',
                            'Ensure internal pay equity',
                            'Offer competitive benefits',
                            'Provide performance-based rewards'
                        ]
                    },
                    {
                        'factor': 'Company Culture',
                        'importance': 'Medium-High',
                        'strategies': [
                            'Define dan communicate values clearly',
                            'Ensure leadership models values',
                            'Create inclusive environment',
                            'Foster collaboration dan teamwork'
                        ]
                    }
                ]
            },
            
            'retention_programs': {
                'high_performer_retention': {
                    'identification': [
                        'Top performance ratings',
                        'High potential assessments',
                        'Critical skill sets',
                        'Difficult to replace roles'
                    ],
                    'retention_tactics': [
                        {
                            'tactic': 'Retention Bonuses',
                            'description': 'Financial incentives to stay for specific period',
                            'structure': 'Lump sum atau installment payments',
                            'considerations': 'Cost vs. replacement cost, market conditions'
                        },
                        {
                            'tactic': 'Accelerated Development',
                            'description': 'Fast-track career advancement opportunities',
                            'components': ['Stretch assignments', 'Leadership programs', 'Mentoring', 'External training'],
                            'timeline': '6-18 months for visible progress'
                        },
                        {
                            'tactic': 'Special Recognition',
                            'description': 'Unique acknowledgment of contributions',
                            'examples': ['Awards ceremonies', 'Executive visibility', 'Speaking opportunities', 'Special projects']
                        }
                    ]
                },
                'new_hire_retention': {
                    'critical_periods': [
                        {
                            'period': 'First 30 Days',
                            'focus': 'Onboarding effectiveness',
                            'key_actions': [
                                'Ensure smooth onboarding process',
                                'Provide clear role expectations',
                                'Facilitate early wins',
                                'Check in frequently'
                            ]
                        },
                        {
                            'period': '90 Days',
                            'focus': 'Integration dan performance',
                            'key_actions': [
                                'Conduct formal 90-day review',
                                'Address any concerns atau issues',
                                'Confirm role fit',
                                'Plan continued development'
                            ]
                        },
                        {
                            'period': '1 Year',
                            'focus': 'Long-term engagement',
                            'key_actions': [
                                'Assess job satisfaction',
                                'Discuss career aspirations',
                                'Provide growth opportunities',
                                'Strengthen relationships'
                            ]
                        }
                    ]
                }
            },
            
            'exit_risk_management': {
                'early_warning_signs': [
                    {
                        'indicator': 'Decreased Performance',
                        'description': 'Decline in work quality atau productivity',
                        'response': 'Performance coaching, identify underlying issues'
                    },
                    {
                        'indicator': 'Reduced Engagement',
                        'description': 'Less participation in meetings, activities',
                        'response': 'One-on-one discussions, re-engagement strategies'
                    },
                    {
                        'indicator': 'Increased Absences',
                        'description': 'More sick days, late arrivals, early departures',
                        'response': 'Check on well-being, address work-life balance'
                    },
                    {
                        'indicator': 'Negative Attitude',
                        'description': 'Complaints, criticism, pessimism',
                        'response': 'Address concerns, improve communication'
                    },
                    {
                        'indicator': 'Withdrawal from Team',
                        'description': 'Less collaboration, social interaction',
                        'response': 'Team building, relationship repair'
                    }
                ],
                'intervention_strategies': [
                    {
                        'strategy': 'Stay Conversations',
                        'timing': 'When risk indicators appear',
                        'approach': 'Open dialogue about concerns dan solutions',
                        'outcomes': 'Action plan to address issues'
                    },
                    {
                        'strategy': 'Role Modification',
                        'timing': 'When job fit is the issue',
                        'approach': 'Adjust responsibilities atau change roles',
                        'outcomes': 'Better alignment dengan interests dan skills'
                    },
                    {
                        'strategy': 'Development Opportunities',
                        'timing': 'When growth is the concern',
                        'approach': 'Provide new challenges dan learning',
                        'outcomes': 'Renewed engagement dan commitment'
                    }
                ]
            }
        }
    
    def _load_offboarding_process(self) -> Dict[str, Any]:
        """
        Data tentang proses offboarding
        """
        return {
            'resignation_process': {
                'resignation_meeting': {
                    'objectives': [
                        'Understand reasons for leaving',
                        'Explore retention possibilities',
                        'Ensure smooth transition',
                        'Maintain positive relationship'
                    ],
                    'discussion_topics': [
                        'Reasons for resignation',
                        'Feedback on role dan company',
                        'Transition timeline dan responsibilities',
                        'Final work date dan notice period'
                    ],
                    'documentation': [
                        'Resignation letter',
                        'Exit interview scheduling',
                        'Transition plan',
                        'Final day logistics'
                    ]
                },
                'notice_period_management': {
                    'standard_notice_periods': {
                        'entry_level': '2 weeks',
                        'mid_level': '3-4 weeks',
                        'senior_level': '4-6 weeks',
                        'executive_level': '8-12 weeks'
                    },
                    'activities_during_notice': [
                        'Knowledge transfer sessions',
                        'Project handover',
                        'Client/stakeholder introductions',
                        'Documentation completion',
                        'Training replacement'
                    ]
                }
            },
            
            'knowledge_transfer': {
                'transfer_methods': [
                    {
                        'method': 'Documentation',
                        'components': [
                            'Process documentation',
                            'Project status reports',
                            'Contact lists dan relationships',
                            'Passwords dan access information'
                        ],
                        'timeline': 'Throughout notice period'
                    },
                    {
                        'method': 'Training Sessions',
                        'components': [
                            'One-on-one training dengan replacement',
                            'Team knowledge sharing sessions',
                            'Client introduction meetings',
                            'System dan tool demonstrations'
                        ],
                        'timeline': 'Final 1-2 weeks'
                    },
                    {
                        'method': 'Shadowing',
                        'components': [
                            'Replacement observes daily activities',
                            'Joint client meetings',
                            'Process walkthroughs',
                            'Q&A sessions'
                        ],
                        'timeline': 'Final week'
                    }
                ],
                'knowledge_capture_checklist': [
                    'Key responsibilities dan processes',
                    'Important contacts dan relationships',
                    'Ongoing projects dan status',
                    'Recurring tasks dan deadlines',
                    'System access dan passwords',
                    'Institutional knowledge dan history',
                    'Best practices dan lessons learned'
                ]
            },
            
            'administrative_tasks': {
                'hr_checklist': [
                    {
                        'task': 'Final Payroll Processing',
                        'details': [
                            'Calculate final pay including unused PTO',
                            'Process expense reimbursements',
                            'Handle benefit terminations',
                            'Arrange COBRA notifications'
                        ],
                        'timing': 'Final pay period'
                    },
                    {
                        'task': 'Asset Recovery',
                        'details': [
                            'Collect company equipment (laptop, phone, etc.)',
                            'Retrieve company credit cards',
                            'Collect keys dan access badges',
                            'Recover company documents'
                        ],
                        'timing': 'Final day'
                    },
                    {
                        'task': 'Access Termination',
                        'details': [
                            'Disable system accounts',
                            'Remove email access',
                            'Cancel building access',
                            'Update security systems'
                        ],
                        'timing': 'End of final day'
                    }
                ],
                'it_checklist': [
                    'Backup personal files',
                    'Transfer file ownership',
                    'Disable user accounts',
                    'Remove system permissions',
                    'Collect hardware dan software',
                    'Update contact lists',
                    'Archive email account'
                ]
            },
            
            'exit_interviews': {
                'interview_objectives': [
                    'Gather honest feedback about experience',
                    'Identify improvement opportunities',
                    'Understand retention factors',
                    'Maintain positive relationship'
                ],
                'interview_questions': [
                    {
                        'category': 'Role dan Responsibilities',
                        'questions': [
                            'What did you enjoy most about your role?',
                            'What aspects were most challenging?',
                            'Did your role match your expectations?',
                            'What would you change about the role?'
                        ]
                    },
                    {
                        'category': 'Management dan Leadership',
                        'questions': [
                            'How would you describe your relationship dengan your manager?',
                            'Did you receive adequate support dan feedback?',
                            'What could leadership do differently?',
                            'How effective was communication from management?'
                        ]
                    },
                    {
                        'category': 'Company Culture',
                        'questions': [
                            'How would you describe the company culture?',
                            'Did you feel valued dan appreciated?',
                            'What did you like most about working here?',
                            'What would you change about the culture?'
                        ]
                    },
                    {
                        'category': 'Development dan Growth',
                        'questions': [
                            'Did you have opportunities for growth?',
                            'What additional training would have been helpful?',
                            'Were your career goals supported?',
                            'What prevented you from advancing?'
                        ]
                    },
                    {
                        'category': 'Reasons for Leaving',
                        'questions': [
                            'What was the primary reason for your decision to leave?',
                            'What could have been done to retain you?',
                            'Would you consider returning in the future?',
                            'Would you recommend this company to others?'
                        ]
                    }
                ],
                'interview_best_practices': [
                    'Conduct interview dengan neutral party (HR)',
                    'Ensure confidentiality dan anonymity',
                    'Ask open-ended questions',
                    'Listen actively without being defensive',
                    'Document feedback for analysis',
                    'Follow up on actionable insights'
                ]
            }
        }
    
    def _load_alumni_relations(self) -> Dict[str, Any]:
        """
        Data tentang alumni relations
        """
        return {
            'alumni_network': {
                'benefits_to_company': [
                    'Potential rehires dengan proven track record',
                    'Referral source for new candidates',
                    'Brand ambassadors in the market',
                    'Business development opportunities',
                    'Industry insights dan intelligence'
                ],
                'benefits_to_alumni': [
                    'Continued professional network',
                    'Access to job opportunities',
                    'Industry updates dan insights',
                    'Professional development resources',
                    'Social connections dan relationships'
                ]
            },
            
            'alumni_engagement': {
                'communication_channels': [
                    {
                        'channel': 'Alumni Newsletter',
                        'frequency': 'Quarterly',
                        'content': [
                            'Company updates dan news',
                            'Alumni spotlights dan achievements',
                            'Industry insights',
                            'Job opportunities',
                            'Event announcements'
                        ]
                    },
                    {
                        'channel': 'LinkedIn Alumni Group',
                        'purpose': 'Professional networking platform',
                        'activities': [
                            'Industry discussions',
                            'Job postings',
                            'Event coordination',
                            'Knowledge sharing'
                        ]
                    },
                    {
                        'channel': 'Alumni Events',
                        'types': [
                            'Annual alumni reunion',
                            'Industry networking events',
                            'Professional development workshops',
                            'Social gatherings'
                        ]
                    }
                ],
                'engagement_activities': [
                    {
                        'activity': 'Mentoring Programs',
                        'description': 'Alumni mentor current employees',
                        'benefits': 'Knowledge transfer, career guidance, network expansion'
                    },
                    {
                        'activity': 'Speaking Opportunities',
                        'description': 'Alumni share expertise at company events',
                        'benefits': 'Thought leadership, knowledge sharing, relationship building'
                    },
                    {
                        'activity': 'Consulting Projects',
                        'description': 'Engage alumni for specialized projects',
                        'benefits': 'Access to expertise, flexible resource, cost-effective'
                    }
                ]
            },
            
            'boomerang_employees': {
                'rehiring_considerations': [
                    {
                        'factor': 'Previous Performance',
                        'evaluation': 'Review past performance records dan feedback',
                        'weight': 'High'
                    },
                    {
                        'factor': 'Reason for Leaving',
                        'evaluation': 'Understand original departure circumstances',
                        'weight': 'High'
                    },
                    {
                        'factor': 'External Experience',
                        'evaluation': 'Assess skills dan knowledge gained elsewhere',
                        'weight': 'Medium'
                    },
                    {
                        'factor': 'Cultural Fit',
                        'evaluation': 'Confirm continued alignment dengan company culture',
                        'weight': 'Medium'
                    },
                    {
                        'factor': 'Team Dynamics',
                        'evaluation': 'Consider impact on current team relationships',
                        'weight': 'Medium'
                    }
                ],
                'rehiring_benefits': [
                    'Reduced onboarding time',
                    'Known performance track record',
                    'Existing relationships dan networks',
                    'Cultural familiarity',
                    'Enhanced skills from external experience'
                ],
                'rehiring_challenges': [
                    'Potential team dynamics issues',
                    'Expectations management',
                    'Salary dan position negotiations',
                    'Integration dengan new team members'
                ]
            }
        }
    
    def get_lifecycle_stage_info(self, stage: str) -> Dict[str, Any]:
        """
        Mendapatkan informasi untuk tahap tertentu dalam employee lifecycle
        """
        stage_mapping = {
            'recruitment': self.recruitment_process,
            'onboarding': self.onboarding_process,
            'performance': self.performance_management,
            'development': self.career_development,
            'engagement': self.employee_engagement,
            'retention': self.retention_strategies,
            'offboarding': self.offboarding_process,
            'alumni': self.alumni_relations
        }
        
        if stage in stage_mapping:
            return {
                'stage': stage,
                'information': stage_mapping[stage],
                'best_practices': self._get_stage_best_practices(stage)
            }
        return {}
    
    def _get_stage_best_practices(self, stage: str) -> List[str]:
        """
        Mendapatkan best practices untuk tahap tertentu
        """
        best_practices = {
            'recruitment': [
                'Use structured interviews for consistency',
                'Implement diverse sourcing strategies',
                'Focus on candidate experience',
                'Measure and optimize recruitment metrics'
            ],
            'onboarding': [
                'Start onboarding before first day',
                'Assign buddy or mentor',
                'Provide clear role expectations',
                'Gather feedback and iterate'
            ],
            'performance': [
                'Set clear, measurable goals',
                'Provide regular feedback',
                'Focus on development, not just evaluation',
                'Use multiple data sources'
            ],
            'development': [
                'Create individual development plans',
                'Offer diverse learning opportunities',
                'Support internal mobility',
                'Measure development ROI'
            ],
            'engagement': [
                'Measure engagement regularly',
                'Act on survey feedback',
                'Recognize and reward contributions',
                'Foster inclusive culture'
            ],
            'retention': [
                'Identify flight risks early',
                'Address root causes of turnover',
                'Invest in high performers',
                'Create compelling employee value proposition'
            ],
            'offboarding': [
                'Conduct thorough exit interviews',
                'Ensure complete knowledge transfer',
                'Maintain positive relationships',
                'Learn from departures'
            ],
            'alumni': [
                'Stay connected with former employees',
                'Leverage alumni network for recruitment',
                'Consider boomerang hiring',
                'Maintain employer brand through alumni'
            ]
        }
        return best_practices.get(stage, [])
    
    def search_lifecycle_info(self, query: str) -> List[Dict[str, Any]]:
        """
        Mencari informasi dalam employee lifecycle berdasarkan query
        """
        results = []
        query_lower = query.lower()
        
        # Search dalam recruitment process
        if any(term in query_lower for term in ['recruitment', 'hiring', 'interview', 'candidate']):
            results.append({
                'category': 'Recruitment Process',
                'relevance': 0.9,
                'data': self.recruitment_process
            })
        
        # Search dalam onboarding
        if any(term in query_lower for term in ['onboarding', 'orientation', 'new hire', 'first day']):
            results.append({
                'category': 'Onboarding Process',
                'relevance': 0.9,
                'data': self.onboarding_process
            })
        
        # Search dalam performance management
        if any(term in query_lower for term in ['performance', 'review', 'evaluation', 'goals']):
            results.append({
                'category': 'Performance Management',
                'relevance': 0.9,
                'data': self.performance_management
            })
        
        # Search dalam career development
        if any(term in query_lower for term in ['career', 'development', 'growth', 'promotion']):
            results.append({
                'category': 'Career Development',
                'relevance': 0.9,
                'data': self.career_development
            })
        
        # Search dalam employee engagement
        if any(term in query_lower for term in ['engagement', 'satisfaction', 'motivation', 'culture']):
            results.append({
                'category': 'Employee Engagement',
                'relevance': 0.9,
                'data': self.employee_engagement
            })
        
        # Search dalam retention
        if any(term in query_lower for term in ['retention', 'turnover', 'quit', 'leave']):
            results.append({
                'category': 'Retention Strategies',
                'relevance': 0.9,
                'data': self.retention_strategies
            })
        
        # Search dalam offboarding
        if any(term in query_lower for term in ['offboarding', 'exit', 'resignation', 'departure']):
            results.append({
                'category': 'Offboarding Process',
                'relevance': 0.9,
                'data': self.offboarding_process
            })
        
        # Search dalam alumni relations
        if any(term in query_lower for term in ['alumni', 'former', 'boomerang', 'rehire']):
            results.append({
                'category': 'Alumni Relations',
                'relevance': 0.9,
                'data': self.alumni_relations
            })
        
        return sorted(results, key=lambda x: x['relevance'], reverse=True)
    
    def get_process_timeline(self, process: str) -> Dict[str, Any]:
        """
        Mendapatkan timeline untuk proses tertentu
        """
        timelines = {
            'recruitment': {
                'total_duration': '6-10 weeks',
                'stages': [
                    {'stage': 'Job Analysis', 'duration': '1-2 weeks'},
                    {'stage': 'Sourcing', 'duration': '2-4 weeks'},
                    {'stage': 'Screening', 'duration': '1-2 weeks'},
                    {'stage': 'Interviewing', 'duration': '2-3 weeks'},
                    {'stage': 'Selection', 'duration': '1 week'},
                    {'stage': 'Offer Negotiation', 'duration': '3-5 days'}
                ]
            },
            'onboarding': {
                'total_duration': '3-6 months',
                'stages': [
                    {'stage': 'Pre-boarding', 'duration': '1-2 weeks before start'},
                    {'stage': 'First Day', 'duration': '1 day'},
                    {'stage': 'First Week', 'duration': '1 week'},
                    {'stage': 'First Month', 'duration': '1 month'},
                    {'stage': 'First Quarter', 'duration': '3 months'},
                    {'stage': 'First Six Months', 'duration': '6 months'}
                ]
            }
        }
        return timelines.get(process, {})
    
    def export_lifecycle_data(self) -> Dict[str, Any]:
        """
        Export semua data employee lifecycle
        """
        return {
            'recruitment_process': self.recruitment_process,
            'onboarding_process': self.onboarding_process,
            'performance_management': self.performance_management,
            'career_development': self.career_development,
            'employee_engagement': self.employee_engagement,
            'retention_strategies': self.retention_strategies,
            'offboarding_process': self.offboarding_process,
            'alumni_relations': self.alumni_relations,
            'export_timestamp': datetime.now().isoformat()
        }