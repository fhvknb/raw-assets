#!/bin/bash

# 日志文件路径
LOG_FILE="/var/log/acme_renew.log"

# 输出日志的函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "====== 开始证书自动更新任务 ======"

# 更新所有证书
/root/.acme.sh/acme.sh --cron --home "/root/.acme.sh" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "证书更新成功，检查是否需要重新启动 Nginx 服务..."

    # 检查是否有证书更新成功
    UPDATED_CERTS=$(grep "Your cert is in" "$LOG_FILE" | wc -l)
    if [ "$UPDATED_CERTS" -gt 0 ]; then
        log "检测到证书已更新，重新启动 Nginx 服务..."

        # 停止 Nginx 服务
        systemctl stop nginx
        if [ $? -eq 0 ]; then
            log "Nginx 服务已停止成功。"
        else
            log "错误：停止 Nginx 服务失败！"
            exit 1
        fi

        # 启动 Nginx 服务
        systemctl start nginx
        if [ $? -eq 0 ]; then
            log "Nginx 服务已启动成功！"
        else
            log "错误：启动 Nginx 服务失败！"
            exit 1
        fi
    else
        log "没有检测到证书更新，无需重新启动服务。"
    fi
else
    log "错误：证书更新失败，请检查日志！"
fi

log "====== 证书自动更新任务结束 ======"