"""系统状态监控工具 - 展示监控和报告功能。

这个模块实现了系统状态监控功能，
展示了如何设计监控和报告系统。
"""

from datetime import datetime

from models.robot import Robot, RobotStatus
from models.task import Task, TaskStatus


class StatusMonitor:
    """系统状态监控器

    提供系统状态监控、统计和报告功能
    展示了如何设计监控系统的最佳实践
    """

    def __init__(self):
        """初始化状态监控器"""
        self._monitoring_start_time = datetime.now()

    def get_robot_utilization(self, robots: list[Robot]) -> dict[str, float]:
        """计算机器人利用率统计。

        Args:
            robots: 机器人列表

        Returns:
            包含利用率统计的字典
        """
        if not robots:
            return {}

        total_robots = len(robots)
        idle_count = sum(1 for r in robots if r.status == RobotStatus.IDLE)
        busy_count = sum(1 for r in robots if r.status == RobotStatus.BUSY)
        charging_count = sum(1 for r in robots if r.status == RobotStatus.CHARGING)
        maintenance_count = sum(
            1 for r in robots if r.status == RobotStatus.MAINTENANCE
        )

        return {
            "total_robots": total_robots,
            "idle_rate": idle_count / total_robots * 100,
            "busy_rate": busy_count / total_robots * 100,
            "charging_rate": charging_count / total_robots * 100,
            "maintenance_rate": maintenance_count / total_robots * 100,
            "availability_rate": (idle_count + busy_count) / total_robots * 100,
        }

    def get_task_completion_stats(self, tasks: list[Task]) -> dict[str, float]:
        """计算任务完成统计。

        Args:
            tasks: 任务列表

        Returns:
            包含任务统计的字典
        """
        if not tasks:
            return {}

        total_tasks = len(tasks)
        pending_count = sum(1 for t in tasks if t.status == TaskStatus.PENDING)
        assigned_count = sum(1 for t in tasks if t.status == TaskStatus.ASSIGNED)
        in_progress_count = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS)
        completed_count = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
        failed_count = sum(1 for t in tasks if t.status == TaskStatus.FAILED)

        return {
            "total_tasks": total_tasks,
            "pending_rate": pending_count / total_tasks * 100,
            "assigned_rate": assigned_count / total_tasks * 100,
            "in_progress_rate": in_progress_count / total_tasks * 100,
            "completion_rate": completed_count / total_tasks * 100,
            "failure_rate": failed_count / total_tasks * 100,
        }

    def get_battery_status(self, robots: list[Robot]) -> dict[str, float]:
        """获取电池状态统计。

        Args:
            robots: 机器人列表

        Returns:
            电池状态统计字典
        """
        if not robots:
            return {}

        battery_levels = [robot.battery_level for robot in robots]

        low_battery_count = sum(1 for level in battery_levels if level < 20)
        critical_battery_count = sum(1 for level in battery_levels if level < 10)

        return {
            "average_battery": sum(battery_levels) / len(battery_levels),
            "min_battery": min(battery_levels),
            "max_battery": max(battery_levels),
            "low_battery_count": low_battery_count,
            "critical_battery_count": critical_battery_count,
            "low_battery_rate": low_battery_count / len(robots) * 100,
        }

    def generate_status_report(self, robots: list[Robot], tasks: list[Task]) -> str:
        """生成系统状态报告。

        Args:
            robots: 机器人列表
            tasks: 任务列表

        Returns:
            格式化的状态报告字符串
        """
        current_time = datetime.now()
        uptime = current_time - self._monitoring_start_time

        robot_stats = self.get_robot_utilization(robots)
        task_stats = self.get_task_completion_stats(tasks)
        battery_stats = self.get_battery_status(robots)

        report: list[str] = []
        report.append("🤖 机器人调度系统状态报告")
        report.append("=" * 50)
        report.append(f"📅 报告时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"⏱️  系统运行时间: {uptime}")
        report.append("")

        # 机器人状态
        report.append("🔧 机器人状态:")
        if robot_stats:
            report.append(f"  总机器人数: {robot_stats['total_robots']}")
            report.append(f"  空闲率: {robot_stats['idle_rate']:.1f}%")
            report.append(f"  忙碌率: {robot_stats['busy_rate']:.1f}%")
            report.append(f"  充电率: {robot_stats['charging_rate']:.1f}%")
            report.append(f"  维护率: {robot_stats['maintenance_rate']:.1f}%")
            report.append(f"  可用率: {robot_stats['availability_rate']:.1f}%")
        else:
            report.append("  无机器人数据")
        report.append("")

        # 任务状态
        report.append("📋 任务状态:")
        if task_stats:
            report.append(f"  总任务数: {task_stats['total_tasks']}")
            report.append(f"  待分配率: {task_stats['pending_rate']:.1f}%")
            report.append(f"  已分配率: {task_stats['assigned_rate']:.1f}%")
            report.append(f"  执行中率: {task_stats['in_progress_rate']:.1f}%")
            report.append(f"  完成率: {task_stats['completion_rate']:.1f}%")
            report.append(f"  失败率: {task_stats['failure_rate']:.1f}%")
        else:
            report.append("  无任务数据")
        report.append("")

        # 电池状态
        report.append("🔋 电池状态:")
        if battery_stats:
            report.append(f"  平均电量: {battery_stats['average_battery']:.1f}%")
            report.append(f"  最低电量: {battery_stats['min_battery']:.1f}%")
            report.append(f"  最高电量: {battery_stats['max_battery']:.1f}%")
            report.append(f"  低电量机器人: {battery_stats['low_battery_count']}台")
            report.append(
                f"  极低电量机器人: {battery_stats['critical_battery_count']}台"
            )
        else:
            report.append("  无电池数据")

        return "\n".join(report)

    def get_system_health_score(self, robots: list[Robot], tasks: list[Task]) -> float:
        """计算系统健康度评分。

        Args:
            robots: 机器人列表
            tasks: 任务列表

        Returns:
            健康度评分(0-100)
        """
        if not robots:
            return 0.0

        robot_stats = self.get_robot_utilization(robots)
        task_stats = self.get_task_completion_stats(tasks) if tasks else {}
        battery_stats = self.get_battery_status(robots)

        # 计算各项指标得分
        availability_score = robot_stats.get("availability_rate", 0) * 0.3
        battery_score = min(battery_stats.get("average_battery", 0), 100) * 0.3

        completion_score = 0.0
        if task_stats:
            completion_rate = task_stats.get("completion_rate", 0)
            failure_rate = task_stats.get("failure_rate", 0)
            completion_score = (completion_rate - failure_rate / 2) * 0.4

        # 总分
        health_score = max(0, availability_score + battery_score + completion_score)
        return min(100, health_score)

    def get_alert_conditions(self, robots: list[Robot], tasks: list[Task]) -> list[str]:
        """检查系统告警条件。

        Args:
            robots: 机器人列表
            tasks: 任务列表

        Returns:
            告警信息列表
        """
        alerts: list[str] = []

        # 检查机器人状态
        if robots:
            battery_stats = self.get_battery_status(robots)
            if battery_stats.get("critical_battery_count", 0) > 0:
                alerts.append(
                    f"⚠️ 有{battery_stats['critical_battery_count']}台机器人电量极低"
                )

            if battery_stats.get("low_battery_rate", 0) > 50:
                alerts.append("⚠️ 超过50%的机器人电量偏低")

            maintenance_count = sum(
                1 for r in robots if r.status == RobotStatus.MAINTENANCE
            )
            if maintenance_count > len(robots) * 0.3:
                alerts.append("⚠️ 超过30%的机器人处于维护状态")

        # 检查任务状态
        if tasks:
            task_stats = self.get_task_completion_stats(tasks)
            if task_stats.get("failure_rate", 0) > 20:
                alerts.append("⚠️ 任务失败率超过20%")

            if task_stats.get("pending_rate", 0) > 50:
                alerts.append("⚠️ 超过50%的任务待分配")

        # 检查系统健康度
        health_score = self.get_system_health_score(robots, tasks)
        if health_score < 60:
            alerts.append(f"⚠️ 系统健康度偏低: {health_score:.1f}分")

        return alerts
