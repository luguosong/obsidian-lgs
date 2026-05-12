# Entity 对照表

| 服务 | Entity | 表名 | 数据库 | Mapper XML |
|------|--------|------|--------|------------|
| services-basic | `User` | `user` | `uocs-basic` | ✅ `UserMapper.xml` |
| services-basic | `Role` | `role` | `uocs-basic` | ✅ `RoleMapper.xml` |
| services-basic | `Permission` | `permission` | `uocs-basic` | ✅ `PermissionMapper.xml` |
| services-basic | `UserRole` | `user_role` | `uocs-basic` | ✅ `UserRoleMapper.xml` |
| services-basic | `RolePermission` | `role_permission` | `uocs-basic` | ✅ `RolePermissionMapper.xml` |
| services-basic | `RoleExclusion` | `role_exclusion` | `uocs-basic` | ✅ `RoleExclusionMapper.xml` |
| services-basic | `GlobalFont` | `global_font` | `uocs-basic` | ✅ `GlobalFontMapper.xml` |
| service-ca | `CaCertificate` | `ca_certificate` | `uocs-ca` | ✅ `CaCertificateMapper.xml` |
| service-ca | `SealCertificate` | `seal_certificate` | `uocs-ca` | ✅ `SealCertificateMapper.xml` |
| service-ca | `CaAuditLog` | `ca_audit_log` | `uocs-ca` | ✅ `CaAuditLogMapper.xml` |
| service-seal | `Seal` | `seal` | `uocs-seal` | ✅ `SealMapper.xml` |
| service-seal | `SealAuthorization` | `seal_authorization` | `uocs-seal` | ✅ `SealAuthorizationMapper.xml` |
| service-seal | `SealStatusChange` | `seal_status_change` | `uocs-seal` | ✅ `SealStatusChangeMapper.xml` |
| service-seal | `SealAuditLog` | `seal_audit_log` | `uocs-seal` | ✅ `SealAuditLogMapper.xml` |
| service-seal | `SealUsageLog` | `seal_usage_log` | `uocs-seal` | ✅ `SealUsageLogMapper.xml` |
| service-seal | `Registration` | `registration` | `uocs-seal` | ✅ `RegistrationMapper.xml` |
| service-seal | `RegistrationApproval` | `registration_approval` | `uocs-seal` | ✅ `RegistrationApprovalMapper.xml` |
| service-seal | `RegistrationAuditLog` | `registration_audit_log` | `uocs-seal` | ✅ `RegistrationAuditLogMapper.xml` |
| service-signer | `AccountBinding` | `account_binding` | `uocs-signer` | ✅ `AccountBindingMapper.xml` |
| service-signer | `SignerSession` | `signer_session` | `uocs-signer` | ✅ `SignerSessionMapper.xml` |
| service-signer | `SealUsageRequest` | `seal_usage_request` | `uocs-signer` | ✅ `SealUsageRequestMapper.xml` |
| service-signer | `CallbackRecord` | `callback_record` | `uocs-signer` | ✅ `CallbackRecordMapper.xml` |
| service-signer | `SealUsagePolicy` | `seal_usage_policy` | `uocs-signer` | ✅ `SealUsagePolicyMapper.xml` |

> **注意**: `services-open-cloud` 没有独立数据库，是 docker compose 中 `open-cloud` 容器（.NET OpenCloud Server，监听 `open-cloud:8001`）的 Spring Cloud 反向代理服务；`service-ra` 是纯 PKI RA 服务，无独立数据库。
