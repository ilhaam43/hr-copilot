# -*- coding: utf-8 -*-
"""
Compliance and Regulatory Data
Berisi informasi tentang compliance, regulasi, dan aspek legal HR
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class ComplianceRegulatoryData:
    """
    Kelas untuk mengelola data compliance dan regulatory
    """
    
    def __init__(self):
        self.labor_laws = self._load_labor_laws()
        self.employment_regulations = self._load_employment_regulations()
        self.workplace_safety = self._load_workplace_safety()
        self.data_privacy = self._load_data_privacy()
        self.equal_opportunity = self._load_equal_opportunity()
        self.compensation_compliance = self._load_compensation_compliance()
        self.leave_policies = self._load_leave_policies()
        self.audit_checklists = self._load_audit_checklists()
    
    def _load_labor_laws(self) -> Dict[str, Any]:
        """
        Data tentang undang-undang ketenagakerjaan
        """
        return {
            'indonesia_labor_law': {
                'uu_no_13_2003': {
                    'title': 'Undang-Undang No. 13 Tahun 2003 tentang Ketenagakerjaan',
                    'key_provisions': {
                        'working_hours': {
                            'regular_hours': '8 jam per hari atau 40 jam per minggu',
                            'overtime_limit': 'Maksimal 3 jam per hari dan 14 jam per minggu',
                            'rest_periods': 'Istirahat minimal 30 menit setelah 4 jam kerja berturut-turut'
                        },
                        'minimum_wage': {
                            'determination': 'Ditetapkan oleh Gubernur berdasarkan rekomendasi Dewan Pengupahan',
                            'review_frequency': 'Setiap tahun',
                            'components': 'Upah pokok + tunjangan tetap minimal 75% dari upah'
                        },
                        'employment_contracts': {
                            'types': [
                                'Perjanjian Kerja Waktu Tertentu (PKWT)',
                                'Perjanjian Kerja Waktu Tidak Tertentu (PKWTT)'
                            ],
                            'pkwt_limitations': {
                                'duration': 'Maksimal 2 tahun, dapat diperpanjang 1 kali maksimal 1 tahun',
                                'renewal': 'Dapat diperbaharui setelah jeda 30 hari',
                                'automatic_conversion': 'Menjadi PKWTT jika melebihi batas waktu'
                            }
                        },
                        'termination': {
                            'valid_reasons': [
                                'Pelanggaran berat',
                                'Ditahan pihak berwajib lebih dari 6 bulan',
                                'Melanggar perjanjian kerja, peraturan perusahaan, atau PKB',
                                'Tidak masuk kerja 5 hari berturut-turut tanpa keterangan'
                            ],
                            'severance_pay': {
                                'formula': 'Berdasarkan masa kerja dan jenis pemutusan',
                                'components': [
                                    'Uang pesangon',
                                    'Uang penghargaan masa kerja',
                                    'Uang penggantian hak'
                                ]
                            }
                        }
                    }
                },
                'uu_no_11_2020': {
                    'title': 'Undang-Undang No. 11 Tahun 2020 tentang Cipta Kerja',
                    'key_changes': {
                        'employment_flexibility': [
                            'Penyederhanaan jenis kontrak kerja',
                            'Fleksibilitas waktu kerja',
                            'Kemudahan alih daya (outsourcing)'
                        ],
                        'severance_calculation': {
                            'new_formula': 'Penyederhanaan perhitungan pesangon',
                            'maximum_limit': 'Maksimal 25 bulan upah'
                        },
                        'foreign_workers': {
                            'permit_simplification': 'Penyederhanaan izin tenaga kerja asing',
                            'skill_transfer': 'Kewajiban transfer keahlian kepada pekerja lokal'
                        }
                    }
                }
            },
            
            'international_standards': {
                'ilo_conventions': {
                    'core_conventions': [
                        {
                            'number': 'C029',
                            'title': 'Forced Labour Convention',
                            'description': 'Prohibition of forced or compulsory labour'
                        },
                        {
                            'number': 'C087',
                            'title': 'Freedom of Association',
                            'description': 'Right to organize and collective bargaining'
                        },
                        {
                            'number': 'C098',
                            'title': 'Right to Organise',
                            'description': 'Protection of the right to organise'
                        },
                        {
                            'number': 'C100',
                            'title': 'Equal Remuneration',
                            'description': 'Equal pay for equal work'
                        },
                        {
                            'number': 'C111',
                            'title': 'Discrimination (Employment)',
                            'description': 'Elimination of discrimination in employment'
                        },
                        {
                            'number': 'C138',
                            'title': 'Minimum Age',
                            'description': 'Minimum age for admission to employment'
                        },
                        {
                            'number': 'C182',
                            'title': 'Worst Forms of Child Labour',
                            'description': 'Prohibition of worst forms of child labour'
                        }
                    ]
                }
            }
        }
    
    def _load_employment_regulations(self) -> Dict[str, Any]:
        """
        Regulasi ketenagakerjaan spesifik
        """
        return {
            'recruitment_compliance': {
                'non_discrimination': {
                    'prohibited_criteria': [
                        'Ras, suku, agama, kepercayaan',
                        'Jenis kelamin (kecuali untuk pekerjaan tertentu)',
                        'Status pernikahan dan kehamilan',
                        'Orientasi seksual',
                        'Disabilitas (jika tidak mempengaruhi kemampuan kerja)',
                        'Afiliasi politik'
                    ],
                    'required_practices': [
                        'Job description yang jelas dan objektif',
                        'Kriteria seleksi yang relevan dengan pekerjaan',
                        'Proses wawancara yang terstruktur',
                        'Dokumentasi keputusan hiring'
                    ]
                },
                'background_checks': {
                    'permitted_checks': [
                        'Verifikasi identitas dan dokumen',
                        'Riwayat pendidikan dan pekerjaan',
                        'Referensi dari employer sebelumnya',
                        'Criminal background (untuk posisi tertentu)'
                    ],
                    'consent_requirements': [
                        'Informed consent dari kandidat',
                        'Disclosure tentang jenis informasi yang dicari',
                        'Hak kandidat untuk mengetahui hasil'
                    ]
                }
            },
            
            'employee_classification': {
                'employee_vs_contractor': {
                    'employee_indicators': [
                        'Kontrol atas cara kerja',
                        'Integrasi dengan bisnis perusahaan',
                        'Eksklusivitas hubungan kerja',
                        'Penyediaan alat dan fasilitas kerja',
                        'Pembayaran gaji tetap'
                    ],
                    'contractor_indicators': [
                        'Independensi dalam metode kerja',
                        'Memiliki bisnis sendiri',
                        'Bekerja untuk multiple clients',
                        'Menggunakan alat sendiri',
                        'Pembayaran per project'
                    ],
                    'misclassification_risks': [
                        'Denda dan sanksi hukum',
                        'Kewajiban membayar benefits retroaktif',
                        'Pajak dan kontribusi sosial',
                        'Tuntutan hukum dari pekerja'
                    ]
                }
            },
            
            'workplace_policies': {
                'required_policies': [
                    {
                        'policy': 'Anti-Harassment and Discrimination',
                        'requirements': [
                            'Clear definition of prohibited conduct',
                            'Reporting procedures',
                            'Investigation process',
                            'Protection against retaliation'
                        ]
                    },
                    {
                        'policy': 'Health and Safety',
                        'requirements': [
                            'Hazard identification and control',
                            'Emergency procedures',
                            'Training requirements',
                            'Incident reporting'
                        ]
                    },
                    {
                        'policy': 'Data Privacy and Confidentiality',
                        'requirements': [
                            'Data collection and use guidelines',
                            'Employee consent procedures',
                            'Data security measures',
                            'Breach notification procedures'
                        ]
                    }
                ]
            }
        }
    
    def _load_workplace_safety(self) -> Dict[str, Any]:
        """
        Data tentang keselamatan dan kesehatan kerja
        """
        return {
            'k3_regulations': {
                'uu_no_1_1970': {
                    'title': 'Undang-Undang No. 1 Tahun 1970 tentang Keselamatan Kerja',
                    'scope': 'Semua tempat kerja dengan 10 atau lebih pekerja',
                    'employer_obligations': [
                        'Menyediakan tempat kerja yang aman',
                        'Menyediakan alat pelindung diri (APD)',
                        'Memberikan pelatihan K3',
                        'Melakukan pemeriksaan kesehatan berkala',
                        'Melaporkan kecelakaan kerja'
                    ]
                },
                'pp_no_50_2012': {
                    'title': 'Peraturan Pemerintah No. 50 Tahun 2012 tentang SMK3',
                    'requirements': {
                        'sms_k3': {
                            'mandatory_for': 'Perusahaan dengan 100+ pekerja atau risiko tinggi',
                            'components': [
                                'Kebijakan K3',
                                'Perencanaan K3',
                                'Pelaksanaan K3',
                                'Pemantauan dan evaluasi',
                                'Peninjauan dan peningkatan'
                            ]
                        },
                        'audit_requirements': {
                            'internal_audit': 'Minimal 1 kali per tahun',
                            'external_audit': 'Setiap 3 tahun oleh lembaga audit terakreditasi'
                        }
                    }
                }
            },
            
            'safety_programs': {
                'hazard_identification': {
                    'methods': [
                        'Job Safety Analysis (JSA)',
                        'Hazard Identification and Risk Assessment (HIRA)',
                        'Safety inspections and audits',
                        'Near-miss reporting',
                        'Employee safety suggestions'
                    ],
                    'risk_categories': [
                        'Physical hazards (noise, vibration, temperature)',
                        'Chemical hazards (toxic substances, fumes)',
                        'Biological hazards (bacteria, viruses)',
                        'Ergonomic hazards (repetitive motion, lifting)',
                        'Psychosocial hazards (stress, violence)'
                    ]
                },
                'safety_training': {
                    'mandatory_training': [
                        'General safety orientation for new employees',
                        'Job-specific safety training',
                        'Emergency response procedures',
                        'Use of personal protective equipment',
                        'Hazard communication'
                    ],
                    'training_frequency': {
                        'initial_training': 'Before starting work',
                        'refresher_training': 'Annually or as needed',
                        'specialized_training': 'Based on job requirements'
                    }
                },
                'incident_management': {
                    'reporting_requirements': {
                        'immediate_reporting': 'Fatal accidents, serious injuries',
                        'written_report': 'Within 24 hours to authorities',
                        'investigation': 'Root cause analysis for all incidents'
                    },
                    'investigation_process': [
                        'Secure the scene',
                        'Gather evidence and witness statements',
                        'Analyze root causes',
                        'Develop corrective actions',
                        'Implement and monitor effectiveness'
                    ]
                }
            }
        }
    
    def _load_data_privacy(self) -> Dict[str, Any]:
        """
        Data tentang privasi dan perlindungan data
        """
        return {
            'indonesia_data_protection': {
                'uu_no_27_2022': {
                    'title': 'Undang-Undang No. 27 Tahun 2022 tentang Pelindungan Data Pribadi',
                    'key_principles': [
                        'Lawfulness, fairness, and transparency',
                        'Purpose limitation',
                        'Data minimization',
                        'Accuracy',
                        'Storage limitation',
                        'Integrity and confidentiality',
                        'Accountability'
                    ],
                    'employee_data_rights': [
                        'Right to information',
                        'Right of access',
                        'Right to rectification',
                        'Right to erasure',
                        'Right to restrict processing',
                        'Right to data portability',
                        'Right to object'
                    ]
                }
            },
            
            'international_standards': {
                'gdpr_compliance': {
                    'applicability': 'Companies processing EU residents\' data',
                    'key_requirements': [
                        'Lawful basis for processing',
                        'Data subject consent',
                        'Data protection by design and default',
                        'Data protection impact assessments',
                        'Breach notification (72 hours)',
                        'Data protection officer appointment'
                    ],
                    'employee_data_processing': {
                        'lawful_bases': [
                            'Contract performance',
                            'Legal obligation',
                            'Legitimate interests',
                            'Consent (limited use in employment)'
                        ],
                        'special_categories': {
                            'definition': 'Health, biometric, genetic data',
                            'additional_protections': 'Explicit consent or specific legal basis required'
                        }
                    }
                }
            },
            
            'hr_data_governance': {
                'data_classification': [
                    {
                        'category': 'Public',
                        'examples': 'Employee directory, job titles',
                        'protection_level': 'Basic'
                    },
                    {
                        'category': 'Internal',
                        'examples': 'Performance reviews, salary bands',
                        'protection_level': 'Standard'
                    },
                    {
                        'category': 'Confidential',
                        'examples': 'Individual salaries, disciplinary records',
                        'protection_level': 'High'
                    },
                    {
                        'category': 'Restricted',
                        'examples': 'Medical records, background checks',
                        'protection_level': 'Maximum'
                    }
                ],
                'retention_policies': {
                    'active_employees': 'Duration of employment + legal requirements',
                    'former_employees': {
                        'personnel_files': '7 years after termination',
                        'payroll_records': '4 years after termination',
                        'medical_records': '30 years or as required by law'
                    },
                    'recruitment_data': {
                        'successful_candidates': 'Converted to employee records',
                        'unsuccessful_candidates': '1 year after recruitment process'
                    }
                }
            }
        }
    
    def _load_equal_opportunity(self) -> Dict[str, Any]:
        """
        Data tentang equal opportunity dan anti-diskriminasi
        """
        return {
            'anti_discrimination_laws': {
                'protected_characteristics': [
                    {
                        'characteristic': 'Race and Ethnicity',
                        'protection_scope': 'All employment decisions',
                        'reasonable_accommodations': 'Cultural and religious practices'
                    },
                    {
                        'characteristic': 'Gender',
                        'protection_scope': 'Equal pay, promotion, harassment prevention',
                        'reasonable_accommodations': 'Pregnancy, breastfeeding facilities'
                    },
                    {
                        'characteristic': 'Religion',
                        'protection_scope': 'Hiring, scheduling, dress code',
                        'reasonable_accommodations': 'Prayer time, religious holidays'
                    },
                    {
                        'characteristic': 'Disability',
                        'protection_scope': 'All aspects of employment',
                        'reasonable_accommodations': 'Workplace modifications, flexible schedules'
                    },
                    {
                        'characteristic': 'Age',
                        'protection_scope': 'Hiring, promotion, termination',
                        'reasonable_accommodations': 'Training adaptations'
                    }
                ]
            },
            
            'harassment_prevention': {
                'types_of_harassment': [
                    {
                        'type': 'Sexual Harassment',
                        'definition': 'Unwelcome sexual advances, requests for sexual favors',
                        'examples': [
                            'Inappropriate comments or jokes',
                            'Unwanted physical contact',
                            'Sexual images or materials',
                            'Quid pro quo propositions'
                        ]
                    },
                    {
                        'type': 'Discriminatory Harassment',
                        'definition': 'Harassment based on protected characteristics',
                        'examples': [
                            'Racial slurs or stereotypes',
                            'Religious mockery',
                            'Disability-related jokes',
                            'Age-related comments'
                        ]
                    },
                    {
                        'type': 'Workplace Bullying',
                        'definition': 'Repeated mistreatment that creates hostile environment',
                        'examples': [
                            'Verbal abuse or threats',
                            'Social isolation',
                            'Sabotage of work',
                            'Excessive criticism'
                        ]
                    }
                ],
                'prevention_strategies': [
                    'Clear anti-harassment policies',
                    'Regular training for all employees',
                    'Multiple reporting channels',
                    'Prompt and thorough investigations',
                    'Appropriate corrective actions',
                    'Protection against retaliation'
                ]
            },
            
            'accommodation_process': {
                'request_procedure': [
                    'Employee submits accommodation request',
                    'HR initiates interactive process',
                    'Assess essential job functions',
                    'Identify potential accommodations',
                    'Evaluate feasibility and cost',
                    'Implement agreed accommodation',
                    'Monitor effectiveness'
                ],
                'types_of_accommodations': [
                    {
                        'category': 'Physical Modifications',
                        'examples': [
                            'Wheelchair accessible workstations',
                            'Ergonomic equipment',
                            'Adjustable desks and chairs',
                            'Accessible parking spaces'
                        ]
                    },
                    {
                        'category': 'Schedule Modifications',
                        'examples': [
                            'Flexible work hours',
                            'Part-time schedules',
                            'Remote work options',
                            'Modified break schedules'
                        ]
                    },
                    {
                        'category': 'Technology Accommodations',
                        'examples': [
                            'Screen readers for visually impaired',
                            'Voice recognition software',
                            'Amplified telephones',
                            'Large print materials'
                        ]
                    }
                ]
            }
        }
    
    def _load_compensation_compliance(self) -> Dict[str, Any]:
        """
        Data tentang compliance kompensasi
        """
        return {
            'wage_hour_laws': {
                'minimum_wage_compliance': {
                    'calculation_basis': 'Regular hourly rate for all hours worked',
                    'inclusions': [
                        'Base salary or hourly wage',
                        'Commissions and bonuses',
                        'Shift differentials',
                        'On-call pay'
                    ],
                    'exclusions': [
                        'Discretionary bonuses',
                        'Gifts and special occasion bonuses',
                        'Reimbursements for expenses',
                        'Premium pay for overtime'
                    ]
                },
                'overtime_regulations': {
                    'overtime_threshold': '40 hours per week (varies by jurisdiction)',
                    'overtime_rate': 'Minimum 1.5x regular rate',
                    'exempt_employees': [
                        'Executive employees',
                        'Administrative employees',
                        'Professional employees',
                        'Outside sales employees'
                    ],
                    'record_keeping': [
                        'Hours worked each day',
                        'Total hours worked each week',
                        'Regular hourly rate',
                        'Overtime hours and pay',
                        'Deductions from pay'
                    ]
                }
            },
            
            'pay_equity_compliance': {
                'equal_pay_principles': [
                    'Equal pay for equal work',
                    'Comparable worth for similar jobs',
                    'Elimination of gender pay gaps',
                    'Transparent pay practices'
                ],
                'pay_equity_analysis': {
                    'statistical_methods': [
                        'Regression analysis controlling for legitimate factors',
                        'Cohort analysis by job level and experience',
                        'Pay range analysis',
                        'Promotion and advancement analysis'
                    ],
                    'legitimate_factors': [
                        'Education and qualifications',
                        'Experience and tenure',
                        'Performance ratings',
                        'Geographic location',
                        'Market rates for position'
                    ]
                },
                'remediation_strategies': [
                    'Immediate salary adjustments for significant gaps',
                    'Phased approach for budget constraints',
                    'Process improvements to prevent future gaps',
                    'Regular monitoring and reporting'
                ]
            },
            
            'benefits_compliance': {
                'mandatory_benefits': [
                    {
                        'benefit': 'Social Security (BPJS Ketenagakerjaan)',
                        'coverage': 'All employees',
                        'employer_contribution': 'Varies by program component'
                    },
                    {
                        'benefit': 'Health Insurance (BPJS Kesehatan)',
                        'coverage': 'All employees and dependents',
                        'employer_contribution': 'Minimum 4% of salary'
                    },
                    {
                        'benefit': 'Annual Leave',
                        'entitlement': 'Minimum 12 working days per year',
                        'accrual': 'After 12 months of continuous service'
                    }
                ],
                'voluntary_benefits': [
                    'Life and disability insurance',
                    'Retirement savings plans',
                    'Flexible spending accounts',
                    'Employee assistance programs',
                    'Wellness programs'
                ]
            }
        }
    
    def _load_leave_policies(self) -> Dict[str, Any]:
        """
        Data tentang kebijakan cuti dan leave
        """
        return {
            'statutory_leave': {
                'annual_leave': {
                    'entitlement': 'Minimum 12 working days per year',
                    'eligibility': 'After 12 months continuous service',
                    'accrual': 'Pro-rated based on service period',
                    'carryover': 'As per company policy, subject to legal limits'
                },
                'sick_leave': {
                    'entitlement': 'As needed with medical certificate',
                    'duration': 'Up to 12 months with full pay, then reduced pay',
                    'documentation': 'Medical certificate required after 2 days'
                },
                'maternity_leave': {
                    'duration': '3 months (1.5 months before, 1.5 months after birth)',
                    'pay': 'Full salary during leave period',
                    'job_protection': 'Right to return to same or equivalent position'
                },
                'paternity_leave': {
                    'duration': '2 days for birth of child',
                    'pay': 'Full salary',
                    'timing': 'Around time of birth'
                }
            },
            
            'religious_cultural_leave': {
                'religious_holidays': {
                    'major_holidays': [
                        'Eid al-Fitr (2 days)',
                        'Eid al-Adha (1 day)',
                        'Christmas Day',
                        'Good Friday',
                        'Vesak Day',
                        'Hindu New Year'
                    ],
                    'accommodation': 'Flexible scheduling for religious observances'
                },
                'cultural_leave': {
                    'traditional_ceremonies': 'Time off for important cultural events',
                    'family_obligations': 'Bereavement leave for family members'
                }
            },
            
            'leave_administration': {
                'request_process': [
                    'Advance notice requirements',
                    'Approval procedures',
                    'Documentation requirements',
                    'Coverage arrangements'
                ],
                'record_keeping': [
                    'Leave balances and accruals',
                    'Leave taken and remaining',
                    'Medical certifications',
                    'Return to work documentation'
                ],
                'compliance_monitoring': [
                    'Ensure minimum leave entitlements',
                    'Track leave usage patterns',
                    'Monitor for leave abuse',
                    'Maintain confidentiality of medical information'
                ]
            }
        }
    
    def _load_audit_checklists(self) -> Dict[str, Any]:
        """
        Checklist untuk audit compliance
        """
        return {
            'hr_compliance_audit': {
                'employment_practices': [
                    {
                        'area': 'Recruitment and Hiring',
                        'checklist_items': [
                            'Job descriptions are current and accurate',
                            'Hiring process is documented and consistent',
                            'Background check procedures comply with law',
                            'Interview questions avoid discriminatory topics',
                            'Hiring decisions are documented with rationale'
                        ]
                    },
                    {
                        'area': 'Employee Classification',
                        'checklist_items': [
                            'Employees properly classified as exempt/non-exempt',
                            'Independent contractors meet legal criteria',
                            'Job descriptions reflect actual duties',
                            'Classification reviews conducted regularly'
                        ]
                    },
                    {
                        'area': 'Compensation and Benefits',
                        'checklist_items': [
                            'Minimum wage requirements met',
                            'Overtime calculations are accurate',
                            'Pay equity analysis conducted',
                            'Benefits administration complies with regulations',
                            'Payroll records are complete and accurate'
                        ]
                    }
                ],
                'workplace_policies': [
                    {
                        'area': 'Anti-Discrimination and Harassment',
                        'checklist_items': [
                            'Policies are current and comprehensive',
                            'Training provided to all employees',
                            'Complaint procedures are effective',
                            'Investigations are prompt and thorough',
                            'Corrective actions are appropriate'
                        ]
                    },
                    {
                        'area': 'Health and Safety',
                        'checklist_items': [
                            'Safety policies and procedures in place',
                            'Hazard assessments conducted regularly',
                            'Safety training provided and documented',
                            'Incident reporting system functional',
                            'Emergency procedures established'
                        ]
                    }
                ],
                'record_keeping': [
                    {
                        'area': 'Personnel Files',
                        'checklist_items': [
                            'Files contain required documents',
                            'Medical information stored separately',
                            'Access to files is controlled',
                            'Retention schedules followed',
                            'Confidentiality maintained'
                        ]
                    },
                    {
                        'area': 'Payroll Records',
                        'checklist_items': [
                            'Time records are accurate and complete',
                            'Wage calculations are correct',
                            'Deductions are authorized and legal',
                            'Records retained for required period',
                            'Tax filings are timely and accurate'
                        ]
                    }
                ]
            },
            
            'audit_frequency': {
                'annual_audits': [
                    'Comprehensive HR compliance review',
                    'Pay equity analysis',
                    'Safety program evaluation',
                    'Policy review and updates'
                ],
                'quarterly_reviews': [
                    'Payroll compliance check',
                    'Leave administration review',
                    'Training completion status',
                    'Incident and complaint tracking'
                ],
                'ongoing_monitoring': [
                    'New hire documentation',
                    'Performance management compliance',
                    'Disciplinary action documentation',
                    'Termination procedures'
                ]
            }
        }
    
    def get_compliance_info(self, category: str, topic: str = None) -> Dict[str, Any]:
        """
        Mendapatkan informasi compliance untuk kategori tertentu
        """
        if hasattr(self, category):
            data = getattr(self, category)
            if topic and isinstance(data, dict) and topic in data:
                return {
                    'category': category,
                    'topic': topic,
                    'information': data[topic],
                    'compliance_tips': self._get_compliance_tips(category, topic)
                }
            return {
                'category': category,
                'information': data,
                'compliance_tips': self._get_compliance_tips(category)
            }
        return {}
    
    def _get_compliance_tips(self, category: str, topic: str = None) -> List[str]:
        """
        Mendapatkan tips compliance
        """
        tips = {
            'labor_laws': [
                'Stay updated with latest regulatory changes',
                'Maintain detailed documentation',
                'Conduct regular compliance training',
                'Seek legal counsel for complex issues'
            ],
            'workplace_safety': [
                'Implement comprehensive safety programs',
                'Provide regular safety training',
                'Conduct routine safety inspections',
                'Maintain accurate incident records'
            ],
            'data_privacy': [
                'Implement data protection by design',
                'Conduct privacy impact assessments',
                'Provide employee privacy training',
                'Maintain data breach response procedures'
            ]
        }
        return tips.get(category, ['Consult with legal and compliance experts'])
    
    def search_compliance_data(self, query: str) -> List[Dict[str, Any]]:
        """
        Mencari data compliance berdasarkan query
        """
        results = []
        categories = [
            'labor_laws', 'employment_regulations', 'workplace_safety',
            'data_privacy', 'equal_opportunity', 'compensation_compliance',
            'leave_policies', 'audit_checklists'
        ]
        
        for category in categories:
            if hasattr(self, category):
                data = getattr(self, category)
                matches = self._search_in_data(data, query.lower(), category)
                results.extend(matches)
        
        return sorted(results, key=lambda x: x.get('relevance', 0), reverse=True)[:15]
    
    def _search_in_data(self, data: Any, query: str, category: str, path: str = "") -> List[Dict[str, Any]]:
        """
        Recursive search in compliance data
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
                        'content': value,
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
        
        if query == key.lower():
            score += 1.0
        elif query in key.lower():
            score += 0.7
        
        if isinstance(value, str):
            if query == value.lower():
                score += 0.8
            elif query in value.lower():
                score += 0.5
        
        return score
    
    def get_audit_checklist(self, audit_type: str) -> Dict[str, Any]:
        """
        Mendapatkan checklist audit untuk tipe tertentu
        """
        if audit_type in self.audit_checklists:
            return {
                'audit_type': audit_type,
                'checklist': self.audit_checklists[audit_type],
                'preparation_tips': [
                    'Review all relevant policies and procedures',
                    'Gather required documentation',
                    'Train staff on audit process',
                    'Conduct pre-audit self-assessment'
                ]
            }
        return {}
    
    def export_compliance_data(self, category: str = None) -> str:
        """
        Export compliance data
        """
        if category and hasattr(self, category):
            data = {category: getattr(self, category)}
        else:
            data = {
                'labor_laws': self.labor_laws,
                'employment_regulations': self.employment_regulations,
                'workplace_safety': self.workplace_safety,
                'data_privacy': self.data_privacy,
                'equal_opportunity': self.equal_opportunity,
                'compensation_compliance': self.compensation_compliance,
                'leave_policies': self.leave_policies,
                'audit_checklists': self.audit_checklists
            }
        
        return json.dumps(data, indent=2, ensure_ascii=False)