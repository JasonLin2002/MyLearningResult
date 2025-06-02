import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def create_oracle_constant_0(qc, qubits):
    """創建常數函數 f(x) = 0 的預言機 (Oracle)"""
    # 不做任何操作，因為 |0⟩ ⊕ 0 = |0⟩
    pass

def create_oracle_constant_1(qc, qubits):
    """創建常數函數 f(x) = 1 的預言機 (Oracle)"""
    # 對輔助量子位元應用 X 閘
    qc.x(qubits[-1])

def create_oracle_balanced(qc, qubits, pattern):
    """創建平衡函數的預言機 (Oracle)"""
    n = len(qubits) - 1  # 輸入量子位元數量
    
    for i in range(n):
        if pattern & (1 << i):
            qc.x(qubits[i])
    
    # 多控制 CNOT 閘 - 實現 |x⟩|y⟩→|x⟩|y⊕f(x)⟩
    if n == 1:
        qc.cx(qubits[0], qubits[-1])
    elif n == 2:
        qc.ccx(qubits[0], qubits[1], qubits[-1])
    else:
        controls = qubits[:-1]
        target = qubits[-1]
        qc.mcx(controls, target)
    
    # 恢復輸入狀態
    for i in range(n):
        if pattern & (1 << i):
            qc.x(qubits[i])

def deutsch_jozsa_algorithm(oracle_type, n_qubits=2, pattern=0):
    """
    實現 Deutsch-Jozsa 演算法 - 對應PDF步驟
    
    Args:
        oracle_type: 'constant_0', 'constant_1', 或 'balanced'
        n_qubits: 輸入量子位元數量 (n個輸入量子位元)
        pattern: 平衡函數的模式
    """
    # 步驟1: 初始化 - 準備 n 個輸入量子位元和 1 個輔助量子位元
    qreg = QuantumRegister(n_qubits + 1, 'q')
    creg = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qreg, creg)
    
    # 初始化輔助量子位元為 |1⟩ (或 |−⟩ 狀態)
    qc.x(qreg[-1])
    
    # 步驟2: 施加 Hadamard 閘 - 創建均勻疊加態
    for i in range(n_qubits + 1):
        qc.h(qreg[i])
    
    qc.barrier()
    
    # 步驟3: 查詢量子黑箱函數 (Oracle) - 相位反饋發生
    if oracle_type == 'constant_0':
        create_oracle_constant_0(qc, qreg)
    elif oracle_type == 'constant_1':
        create_oracle_constant_1(qc, qreg)
    elif oracle_type == 'balanced':
        create_oracle_balanced(qc, qreg, pattern)
    
    qc.barrier()
    
    # 步驟4: 再次施加 Hadamard 閘 - 干涉效應
    for i in range(n_qubits):
        qc.h(qreg[i])
    
    # 步驟5: 測量 n 個輸入量子位元的最終狀態
    for i in range(n_qubits):
        qc.measure(qreg[i], creg[i])
    
    return qc

def run_experiment(oracle_type, n_qubits=2, pattern=0, shots=1024):
    """運行實驗並返回結果"""
    qc = deutsch_jozsa_algorithm(oracle_type, n_qubits, pattern)
    
    # 使用模擬器
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=shots).result()
    counts = result.get_counts()
    
    return qc, counts

def analyze_result(counts, function_type):
    """分析結果並判斷函數類型"""
    all_zero = '00' in counts and len(counts) == 1
    if all_zero:
        conclusion = "常數函數"
        quantum_advantage = "✓ 單次查詢成功識別"
    else:
        conclusion = "平衡函數"
        quantum_advantage = "✓ 單次查詢成功識別"
    
    print(f"函數類型: {function_type}")
    print(f"測量結果: {counts}")
    print(f"演算法判斷: {conclusion}")
    print(f"量子優勢: {quantum_advantage}")
    print("-" * 50)

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

qc1, counts1 = run_experiment('constant_0', n_qubits=2)
analyze_result(counts1, "常數函數 f(x) = 0")

qc2, counts2 = run_experiment('constant_1', n_qubits=2)
analyze_result(counts2, "常數函數 f(x) = 1")

qc3, counts3 = run_experiment('balanced', n_qubits=2, pattern=1)
analyze_result(counts3, "平衡函數")

# 繪製量子電路圖
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

qc1.draw('mpl', ax=axes[0])
axes[0].set_title('常數函數 f(x) = 0', fontsize=14)

qc2.draw('mpl', ax=axes[1]) 
axes[1].set_title('常數函數 f(x) = 1', fontsize=14)

qc3.draw('mpl', ax=axes[2])
axes[2].set_title('平衡函數', fontsize=14)

plt.tight_layout()
plt.show()