from coze_coding_dev_sdk.database import Base

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, Integer, Numeric, PrimaryKeyConstraint, Table, Text, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy import String, Float, func
from typing import Optional
import datetime

from sqlalchemy.orm import Mapped, mapped_column

class HealthCheck(Base):
    __tablename__ = 'health_check'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='health_check_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class Reminder(Base):
    """提醒任务表"""
    __tablename__ = 'reminders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='reminders_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_message: Mapped[str] = mapped_column(Text, nullable=False, comment="用户消息内容")
    remind_time: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, comment="提醒时间")
    sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否已发送")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False, comment="创建时间")


class ExerciseRecord(Base):
    """运动记录表"""
    __tablename__ = 'exercise_records'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='exercise_records_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_message: Mapped[str] = mapped_column(Text, nullable=False, comment="用户消息内容")
    exercise_type: Mapped[str] = mapped_column(String(100), nullable=False, comment="运动类型")
    duration: Mapped[int] = mapped_column(Integer, nullable=False, comment="运动时长（分钟）")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="用户描述/体验")
    calories_burned: Mapped[float] = mapped_column(Float, nullable=False, comment="燃烧热量（千卡）")
    month_total_duration: Mapped[int] = mapped_column(Integer, nullable=False, comment="本月总时长（分钟）")
    month_calories_equivalent: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="本月总热量对应肉类")
    encouragement_message: Mapped[str] = mapped_column(Text, nullable=False, comment="鼓励语")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False, comment="创建时间")
