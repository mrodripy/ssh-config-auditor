#!/usr/bin/env python3
"""Pruebas básicas para el SSH Configuration Auditor."""

import unittest
import tempfile
import os
import sys

# Agregar src al path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ssh_audit import SSHAuditor

class TestSSHAuditor(unittest.TestCase):
    """Clase de pruebas para SSHAuditor."""
    
    def setUp(self):
        """Configuración antes de cada prueba."""
        # Crear un archivo baseline temporal
        self.baseline_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.baseline_file.write("Protocol 2\nPermitRootLogin no\n")
        self.baseline_file.close()
        
        # Crear un archivo config temporal
        self.config_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.config_file.write("Protocol 2\nPermitRootLogin yes\n")
        self.config_file.close()
        
    def tearDown(self):
        """Limpieza después de cada prueba."""
        os.unlink(self.baseline_file.name)
        os.unlink(self.config_file.name)
    
    def test_auditor_initialization(self):
        """Prueba que el auditor se inicializa correctamente."""
        auditor = SSHAuditor(self.baseline_file.name)
        self.assertIsInstance(auditor, SSHAuditor)
        self.assertIsInstance(auditor.baseline_rules, dict)
    
    def test_baseline_loading(self):
        """Prueba que el baseline se carga correctamente."""
        auditor = SSHAuditor(self.baseline_file.name)
        self.assertIn('Protocol', auditor.baseline_rules)
        self.assertEqual(auditor.baseline_rules['Protocol'], '2')
    
    def test_audit_file_exists(self):
        """Prueba auditoría de archivo existente."""
        auditor = SSHAuditor(self.baseline_file.name)
        findings = auditor.audit_file(self.config_file.name)
        self.assertIsInstance(findings, list)
        self.assertGreater(len(findings), 0)
    
    def test_audit_file_not_found(self):
        """Prueba auditoría de archivo no existente."""
        auditor = SSHAuditor(self.baseline_file.name)
        findings = auditor.audit_file('/ruta/inexistente/archivo.conf')
        self.assertEqual(len(findings), 0)

if __name__ == '__main__':
    unittest.main()
