import http from 'k6/http';
import { Trend, Counter } from 'k6/metrics';
import { check, sleep } from 'k6';

const statusTrend = new Trend('status_codes');
const successCounter = new Counter('successful_requests');
const errorCounter = new Counter('error_requests');

export const options = {
    // Para los alumnos que siguen prefiriendo Windows 11 es posible que tengan que descomentar insecureSkipTLSVerify
    // insecureSkipTLSVerify: true,
    stages: [
        { duration: "10s", target: 100 },  // Ramp-up a 100 usuarios
        { duration: "20s", target: 100 },  // Mantener 100 usuarios
        { duration: "10s", target: 0 },    // Ramp-down a 0
    ],
};

export default function () {
    // Usar localhost:8000 directamente sin Traefik
    const BASE_URL = 'http://localhost:8000';
    
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    // Test 1: Health check
    const healthRes = http.get(`${BASE_URL}/health/`, params);
    statusTrend.add(healthRes.status);
    
    const healthCheck = check(healthRes, {
        'health check is 200': (r) => r.status === 200,
    });
    
    if (healthCheck) {
        successCounter.add(1);
    } else {
        errorCounter.add(1);
        console.log(`Health check failed: status=${healthRes.status}`);
    }
    
    sleep(0.1);
    
    // Test 2: Listar estudiantes
    const studentsRes = http.get(`${BASE_URL}/students/`, params);
    statusTrend.add(studentsRes.status);
    
    const studentsCheck = check(studentsRes, {
        'students list is 200': (r) => r.status === 200,
        'response is json': (r) => r.headers['Content-Type']?.includes('application/json'),
        'no server errors': (r) => r.status < 500,
    });
    
    if (studentsCheck) {
        successCounter.add(1);
    } else {
        errorCounter.add(1);
        console.log(`Students list failed: status=${studentsRes.status}`);
    }
    
    sleep(0.1);
    
    // Test 3: Listar tipos de documento
    const docTypesRes = http.get(`${BASE_URL}/document-types/`, params);
    statusTrend.add(docTypesRes.status);
    
    const docTypesCheck = check(docTypesRes, {
        'document types list is 200': (r) => r.status === 200,
        'response is json': (r) => r.headers['Content-Type']?.includes('application/json'),
        'no server errors': (r) => r.status < 500,
    });
    
    if (docTypesCheck) {
        successCounter.add(1);
    } else {
        errorCounter.add(1);
        console.log(`Document types list failed: status=${docTypesRes.status}`);
    }
    
    sleep(0.1);
    
    // Test 4: Crear un tipo de documento si no existe
    const docTypesData = JSON.parse(docTypesRes.body);
    let documentTypeId = null;
    
    if (docTypesData.results && docTypesData.results.length > 0) {
        documentTypeId = docTypesData.results[0].id;
    } else {
        // Crear un tipo de documento
        const newDocType = JSON.stringify({
            name: "DNI",
            description: "Documento Nacional de Identidad"
        });
        
        const createDocTypeRes = http.post(`${BASE_URL}/document-types/`, newDocType, params);
        statusTrend.add(createDocTypeRes.status);
        
        if ([200, 201].includes(createDocTypeRes.status)) {
            const docTypeData = JSON.parse(createDocTypeRes.body);
            documentTypeId = docTypeData.id;
            successCounter.add(1);
        } else {
            errorCounter.add(1);
        }
    }
    
    sleep(0.1);
    
    // Test 5: Crear un estudiante solo si tenemos un document_type válido
    if (documentTypeId) {
        const newStudent = JSON.stringify({
            first_name: "Test",
            last_name: "Student",
            document_number: `TEST${Date.now()}${Math.floor(Math.random() * 1000)}`,
            birth_date: "2000-01-01",
            gender: "M",
            student_number: Date.now() + Math.floor(Math.random() * 100000),
            enrollment_date: "2025-01-01",
            document_type: documentTypeId,
            specialty_id: 1
        });
        
        const createRes = http.post(`${BASE_URL}/students/`, newStudent, params);
        statusTrend.add(createRes.status);
        
        const createCheck = check(createRes, {
            'student created': (r) => [200, 201].includes(r.status),
            'response is valid': (r) => r.status < 500,
        });
        
        if (createCheck) {
            successCounter.add(1);
        } else {
            errorCounter.add(1);
            console.log(`Create student failed: status=${createRes.status}, body=${createRes.body}`);
        }
    }
}
