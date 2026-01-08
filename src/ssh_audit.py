#!/usr/bin/env python3
"""
SSH Configuration Auditor - Fase 1
Herramienta para auditar archivos de configuración SSH contra mejores prácticas.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

class SSHAuditor:
    """Clase principal para auditar configuraciones SSH."""
    
    def __init__(self, baseline_path: str = None):
        """
        Inicializa el auditor con un baseline de seguridad.
        
        Args:
            baseline_path: Ruta al archivo con configuraciones seguras (baseline)
        """
        self.baseline_path = baseline_path
        self.baseline_rules = self._load_baseline() if baseline_path else {}
        self.findings = []
        
    def _load_baseline(self) -> Dict[str, str]:
        """Carga las reglas de seguridad desde el archivo baseline."""
        rules = {}
        try:
            with open(self.baseline_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Maneja líneas con y sin valor
                        if ' ' in line:
                            key, value = line.split(' ', 1)
                            rules[key] = value
                        else:
                            rules[line] = None
            print(f"[+] Baseline cargado: {len(rules)} reglas de seguridad")
            return rules
        except FileNotFoundError:
            print(f"[-] Error: Archivo baseline no encontrado: {self.baseline_path}")
            return {}
    
    def audit_file(self, config_path: str) -> List[Dict]:
        """
        Audita un archivo de configuración SSH.
        
        Args:
            config_path: Ruta al archivo sshd_config a auditar
            
        Returns:
            Lista de hallazgos (findings) con detalles de cada regla
        """
        if not Path(config_path).exists():
            print(f"[-] Error: Archivo no encontrado: {config_path}")
            return []
        
        self.findings = []
        print(f"[+] Auditing: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                config_lines = f.readlines()
            
            # Convierte líneas de configuración a diccionario
            config_dict = {}
            for line in config_lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 2:
                        config_dict[parts[0]] = ' '.join(parts[1:])
                    elif len(parts) == 1:
                        config_dict[parts[0]] = None
            
            # Realiza las comprobaciones contra el baseline
            self._check_configuration(config_dict)
            
            print(f"[+] Auditoría completada: {len(self.findings)} hallazgos")
            return self.findings
            
        except Exception as e:
            print(f"[-] Error al procesar el archivo: {e}")
            return []
    
    def _check_configuration(self, config: Dict[str, str]) -> None:
        """Compara la configuración contra las reglas del baseline."""
        for rule, expected_value in self.baseline_rules.items():
            finding = {
                'rule': rule,
                'expected': expected_value,
                'actual': None,
                'status': 'NOT_FOUND',
                'severity': 'MEDIUM'
            }
            
            if rule in config:
                finding['actual'] = config[rule]
                if config[rule] == expected_value:
                    finding['status'] = 'COMPLIANT'
                    finding['severity'] = 'LOW'
                else:
                    finding['status'] = 'NON_COMPLIANT'
                    # Asigna severidad basada en la regla
                    if rule in ['PermitRootLogin', 'PasswordAuthentication']:
                        finding['severity'] = 'HIGH'
            else:
                # La regla no está en el archivo config
                finding['status'] = 'NOT_SET'
                if rule in ['PermitRootLogin', 'Protocol']:
                    finding['severity'] = 'HIGH'
            
            self.findings.append(finding)
    
    def generate_report(self, findings: List[Dict], output_format: str = 'text') -> str:
        """
        Genera un reporte de los hallazgos.
        
        Args:
            findings: Lista de hallazgos de la auditoría
            output_format: Formato del reporte ('text', 'json')
            
        Returns:
            Reporte formateado
        """
        if output_format == 'json':
            return json.dumps(findings, indent=2)
        
        # Formato texto por defecto
        report_lines = ["=" * 60]
        report_lines.append("SSH CONFIGURATION AUDIT REPORT")
        report_lines.append("=" * 60)
        
        # Contadores
        stats = {'COMPLIANT': 0, 'NON_COMPLIANT': 0, 'NOT_FOUND': 0, 'NOT_SET': 0}
        
        for finding in findings:
            stats[finding['status']] = stats.get(finding['status'], 0) + 1
            
            symbol = {
                'COMPLIANT': '✅',
                'NON_COMPLIANT': '❌',
                'NOT_FOUND': '⚠️',
                'NOT_SET': '🔶'
            }.get(finding['status'], '❓')
            
            report_lines.append(
                f"{symbol} {finding['rule']}: "
                f"Expected='{finding['expected']}', "
                f"Actual='{finding['actual']}' | "
                f"Status: {finding['status']} ({finding['severity']})"
            )
        
        # Resumen
        report_lines.append("\n" + "=" * 60)
        report_lines.append("SUMMARY")
        report_lines.append("=" * 60)
        report_lines.append(f"Total Rules Checked: {len(findings)}")
        report_lines.append(f"✅ Compliant: {stats['COMPLIANT']}")
        report_lines.append(f"❌ Non-Compliant: {stats['NON_COMPLIANT']}")
        report_lines.append(f"⚠️  Not Found in Config: {stats['NOT_FOUND']}")
        report_lines.append(f"🔶 Not Set (Missing): {stats['NOT_SET']}")
        
        return "\n".join(report_lines)

def main():
    """Función principal para ejecución desde línea de comandos."""
    parser = argparse.ArgumentParser(
        description='SSH Configuration Auditor - Fase 1',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'config_file',
        help='Ruta al archivo de configuración SSH a auditar'
    )
    
    parser.add_argument(
        '-b', '--baseline',
        default='configs/cis_baseline.conf',
        help='Ruta al archivo baseline de seguridad (default: configs/cis_baseline.conf)'
    )
    
    parser.add_argument(
        '-o', '--output',
        choices=['text', 'json'],
        default='text',
        help='Formato del reporte de salida (default: text)'
    )
    
    parser.add_argument(
        '-f', '--output-file',
        help='Guardar reporte en un archivo (en lugar de imprimir en pantalla)'
    )
    
    args = parser.parse_args()
    
    # Crear auditor y ejecutar
    auditor = SSHAuditor(args.baseline)
    findings = auditor.audit_file(args.config_file)
    
    if findings:
        report = auditor.generate_report(findings, args.output)
        
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(report)
            print(f"[+] Reporte guardado en: {args.output_file}")
        else:
            print(report)

if __name__ == '__main__':
    main()
