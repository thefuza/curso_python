-- 1. Criação do banco de dados (opcional, caso ainda não exista)
CREATE DATABASE IF NOT EXISTS db_gestao_diligencias;
USE db_gestao_diligencias;

-- 2. Criação da tabela com as colunas correspondentes ao seu dicionário
CREATE TABLE IF NOT EXISTS tb_gestao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    saj VARCHAR(50) NOT NULL,
    sei VARCHAR(50),
    diligencia TEXT,
    secretaria VARCHAR(100),
    prazo DATE,
    status VARCHAR(50),
    dias_restantes INT
);

USE db_gestao_diligencias;

CREATE TABLE IF NOT EXISTS tb_concluidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    saj VARCHAR(50) NOT NULL,
    sei VARCHAR(50),
    diligencia TEXT,
    secretaria VARCHAR(100),
    prazo DATE,
    data_conclusao DATETIME
);

ALTER TABLE tb_gestao ADD COLUMN data_envio DATE;
ALTER TABLE tb_concluidas ADD COLUMN data_envio DATE;

-- Criação do banco de dados para a Lotação Usucapião
CREATE DATABASE IF NOT EXISTS db_gestao_usucapiao;
USE db_gestao_usucapiao;

-- Tabela principal de Usucapião
CREATE TABLE IF NOT EXISTS tb_usucapiao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    saj VARCHAR(30),
    sei VARCHAR(30),
    interessado VARCHAR(150),
    secretarias VARCHAR(255),
    data_envio DATE,
    tipo_solicitacao VARCHAR(30), -- 'Judicial' ou 'Extrajudicial'
    sec1_ok TINYINT DEFAULT 0,    -- 0 = Pendente, 1 = Respondido
    sec2_ok TINYINT DEFAULT 0,
    sec3_ok TINYINT DEFAULT 0,
    status VARCHAR(60)
);

-- Tabela de Usucapião Concluídas
CREATE TABLE IF NOT EXISTS tb_usucapiao_concluidas (
    id INT PRIMARY KEY,
    saj VARCHAR(30),
    sei VARCHAR(30),
    interessado VARCHAR(150),
    secretarias VARCHAR(255),
    data_envio DATE,
    tipo_solicitacao VARCHAR(30),
    data_conclusao DATETIME
);

-- ==========================================
-- 1. ESTRUTURA DE USUÁRIOS E AUDITORIA - DILIGÊNCIAS
-- ==========================================
USE db_gestao_diligencias;

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS tb_usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) NOT NULL -- 'admin' ou 'usuario'
);

-- Inserir usuário administrador padrão (se não existir)
INSERT IGNORE INTO tb_usuarios (id, login, senha, perfil) VALUES (1, 'admin', 'root', 'admin');

-- Adicionar colunas de auditoria na fila ativa
ALTER TABLE tb_gestao 
ADD COLUMN usuario_criacao VARCHAR(50),
ADD COLUMN data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP;

-- Adicionar colunas de auditoria na fila de concluídas
ALTER TABLE tb_concluidas 
ADD COLUMN usuario_criacao VARCHAR(50),
ADD COLUMN data_criacao DATETIME,
ADD COLUMN usuario_conclusao VARCHAR(50);


-- ==========================================
-- 2. ESTRUTURA DE AUDITORIA - USUCAPIÃO
-- ==========================================
USE db_gestao_usucapiao;

-- Adicionar colunas de auditoria na fila ativa
ALTER TABLE tb_usucapiao 
ADD COLUMN usuario_criacao VARCHAR(50),
ADD COLUMN data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP;

-- Adicionar colunas de auditoria na fila de concluídas
ALTER TABLE tb_usucapiao_concluidas 
ADD COLUMN usuario_criacao VARCHAR(50),
ADD COLUMN data_criacao DATETIME,
ADD COLUMN usuario_conclusao VARCHAR(50);