-- Create Database and Schema if they don't exist
CREATE DATABASE IF NOT EXISTS LEGA_DB;
USE DATABASE LEGA_DB;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- Create the Bill Cache table
CREATE TABLE IF NOT EXISTS BILL_CACHE (
    BILL_ID VARCHAR PRIMARY KEY,
    STATE VARCHAR,
    RAW_TEXT VARIANT, -- Storing as Variant to handle potential JSON or large text with structure
    SUMMARY_JSON VARIANT, -- JSON output from Gemini
    AUDIO_URL VARCHAR, -- URL from ElevenLabs
    LAST_UPDATED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
