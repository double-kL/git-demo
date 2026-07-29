import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    """离散 PID 控制器，带积分抗饱和与微分滤波"""
    def __init__(self, Kp, Ki, Kd, dt, setpoint=0,
                 integral_limit=1.0, derivative_filter_alpha=0.1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.setpoint = setpoint

        self.integral_limit = integral_limit
        self.alpha = derivative_filter_alpha   # 一阶低通滤波系数

        self.prev_error = 0.0
        self.integral = 0.0
        self.filtered_derivative = 0.0

    def update(self, measurement):
        error = self.setpoint - measurement

        # 比例项
        P = self.Kp * error

        # 积分项（梯形法 + 抗饱和）
        self.integral += error * self.dt
        self.integral = np.clip(self.integral, -self.integral_limit, self.integral_limit)
        I = self.Ki * self.integral

        # 微分项（基于测量值微分，避免“微分冲击”，并加低通滤波）
        # 使用测量值的负变化率： -d(measurement)/dt  ≈ -(measurement - prev_measurement)/dt
        raw_derivative = -(measurement - self.prev_error) / self.dt  # prev_error 这里复用了存储
        self.filtered_derivative = (self.alpha * raw_derivative +
                                    (1 - self.alpha) * self.filtered_derivative)
        D = self.Kd * self.filtered_derivative

        # 控制器输出
        output = P + I + D

        # 更新状态
        self.prev_error = measurement   # 保存当前测量值用于下一时刻微分
        return output

    def set_setpoint(self, sp):
        self.setpoint = sp


class CarSpeedSystem:
    """简化的小车速度模型：一阶惯性环节
       tau * dv/dt + v = K * u  (u为油门/力，v为速度)
       离散化：v[k+1] = v[k] + (dt/tau) * (K*u[k] - v[k])
    """
    def __init__(self, tau=2.0, K=1.0, dt=0.01):
        self.tau = tau
        self.K = K
        self.dt = dt
        self.v = 0.0          # 初始速度

    def update(self, u):
        # 欧拉法更新
        dv = (self.dt / self.tau) * (self.K * u - self.v)
        self.v += dv
        return self.v


def run_simulation():
    # 时间设置
    dt = 0.01
    sim_time = 20.0
    n_steps = int(sim_time / dt)
    time = np.linspace(0, sim_time, n_steps)

    # 创建被控对象
    system = CarSpeedSystem(tau=2.0, K=1.0, dt=dt)

    # 创建 PID 控制器（这里使用 PI 控制即可无静差）
    # 参数调节示例：Kp=2.0, Ki=1.0, Kd=0.5 （可根据需要调整）
    pid = PIDController(Kp=3.0, Ki=3.0, Kd=0.5, dt=dt,
                        setpoint=10.0, integral_limit=5.0)

    # 存储数据
    velocity_record = np.zeros(n_steps)
    setpoint_record = np.zeros(n_steps)
    control_signal = np.zeros(n_steps)

    # 仿真主循环
    for i in range(n_steps):
        t = time[i]

        # 在 t=2s 时改变目标速度，并在 t=10s 时加入外部扰动
        if t >= 2.0:
            pid.set_setpoint(15.0)
        else:
            pid.set_setpoint(10.0)

        # 测量当前速度
        current_velocity = system.v

        # 控制器计算控制量
        u = pid.update(current_velocity)

        # 加入扰动：在 t=10~12 秒模拟上坡阻力（额外减速加速度）
        disturbance = 0.0
        if 10.0 <= t <= 12.0:
            disturbance = -2.0   # 相当于阻力加速度

        # 系统更新（控制量 + 扰动作为系统输入）
        # 对于速度模型，扰动直接叠加到加速度项上
        u_total = u + disturbance
        system.update(u_total)

        # 记录数据
        velocity_record[i] = current_velocity
        setpoint_record[i] = pid.setpoint
        control_signal[i] = u

    # 绘制结果
    plt.figure(figsize=(12, 8))

    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(time, setpoint_record, 'r--', label='Target Speed')
    ax1.plot(time, velocity_record, 'b-', label='Actual Speed')
    ax1.set_ylabel('Speed (m/s)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_title('PID Speed Control Simulation')

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(time, control_signal, 'g-', label='Control Signal (throttle)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Control Output')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()