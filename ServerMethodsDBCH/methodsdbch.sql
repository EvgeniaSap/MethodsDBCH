--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.24
-- Dumped by pg_dump version 9.5.5

-- Started on 2022-06-02 06:14:25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 11791)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2246 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 693 (class 1247 OID 172045)
-- Name: essence_change; Type: TYPE; Schema: public; Owner: evgenia
--

CREATE TYPE essence_change AS ENUM (
    'Добавление',
    'Изменение',
    'Удаление'
);


ALTER TYPE essence_change OWNER TO evgenia;

--
-- TOC entry 274 (class 1255 OID 163882)
-- Name: auth_user(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION auth_user(loginuser character varying, passworduser character varying) RETURNS TABLE(id_user integer, id_access_level integer, login character varying, password character varying, name_user character varying, name_access_level character varying, status_account integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "users"."id_user", 
			    "users"."id_access_level",
			    "users"."login", 
			    "users"."password",
			    "users"."name_user", 
			    "access_levels"."name_access_level",
			    "users"."status_account"
			    FROM "users"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "users"."status_account" = 0 AND "users"."login" = loginuser AND "users"."password" = passworduser;
 END 		    
$$;


ALTER FUNCTION public.auth_user(loginuser character varying, passworduser character varying) OWNER TO evgenia;

--
-- TOC entry 217 (class 1255 OID 155656)
-- Name: check_password(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION check_password(userlogin character varying, userpsw character varying) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE 
  result BOOLEAN;
BEGIN
SELECT INTO result userpsw ="users"."password" AS tresult
FROM "users"
WHERE "users"."login" = userlogin AND "users"."status_account" = 0;
IF NOT FOUND THEN
  RETURN false;
END IF;
RETURN result;
END
$$;


ALTER FUNCTION public.check_password(userlogin character varying, userpsw character varying) OWNER TO evgenia;

--
-- TOC entry 282 (class 1255 OID 196623)
-- Name: del_method_constraint(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION del_method_constraint(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER DEFAULT 1;
	entrycount integer;
BEGIN
	DELETE FROM "method_constraint"
	WHERE "id_method" = idfirst AND "id_possib_constraint" = idsecond;
	RETURN result;
END
$$;


ALTER FUNCTION public.del_method_constraint(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 243 (class 1255 OID 196624)
-- Name: del_method_constraint(integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION del_method_constraint(idfirst integer, namesecond character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER DEFAULT 1;
	entrycount integer;
	idsecond INTEGER DEFAULT (SELECT "id_possib_constraint" FROM "possib_constraint" WHERE "name_possib_constraint"=namesecond);
BEGIN
	DELETE FROM "method_constraint"
	WHERE "id_method" = idfirst AND "id_possib_constraint" = idsecond;
	RETURN result;
END
$$;


ALTER FUNCTION public.del_method_constraint(idfirst integer, namesecond character varying) OWNER TO evgenia;

--
-- TOC entry 287 (class 1255 OID 196631)
-- Name: del_method_logbook_simp(integer, integer, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION del_method_logbook_simp(idmeth integer, iduser integer, datech date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	idmethod INTEGER;
	idlogbook INTEGER;
BEGIN
	idlogbook = (SELECT * FROM new_logbook_update(idmethod, iduser, 'Удаление', datech));
	result = idlogbook;
	RETURN result;
END
$$;


ALTER FUNCTION public.del_method_logbook_simp(idmeth integer, iduser integer, datech date) OWNER TO evgenia;

--
-- TOC entry 278 (class 1255 OID 196619)
-- Name: del_method_task_area(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION del_method_task_area(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER DEFAULT 1;
	entrycount integer;
BEGIN
	DELETE FROM "method_task_area"
	WHERE "id_method" = idfirst AND "id_task_area" = idsecond;
	RETURN result;
END
$$;


ALTER FUNCTION public.del_method_task_area(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 281 (class 1255 OID 196622)
-- Name: del_method_theorem(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION del_method_theorem(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER DEFAULT 1;
	entrycount integer;
BEGIN
	DELETE FROM "method_theorem"
	WHERE "id_method" = idfirst AND "id_theorem" = idsecond;
	RETURN result;
END
$$;


ALTER FUNCTION public.del_method_theorem(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 279 (class 1255 OID 196620)
-- Name: del_pract_task_area(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION del_pract_task_area(namefirst character varying, namesecond character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER DEFAULT 1;
	entrycount integer;
	idfirst INTEGER DEFAULT (SELECT "id_task_area" FROM "task_area" WHERE "name_task_area"=namefirst);
	idsecond INTEGER DEFAULT (SELECT "id_practical_task" FROM "practical_task" WHERE "name_practical_task"=namesecond);
BEGIN
	DELETE FROM "pract_task_area"
	WHERE "id_task_area" = idfirst AND "id_practical_task" = idsecond;
	RETURN result;
END
$$;


ALTER FUNCTION public.del_pract_task_area(namefirst character varying, namesecond character varying) OWNER TO evgenia;

--
-- TOC entry 229 (class 1255 OID 163879)
-- Name: get_accesslevels(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_accesslevels() RETURNS TABLE(name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "access_levels"."name_access_level"
			    FROM "access_levels"
			    ORDER BY "access_levels"."id_access_level";
END
$$;


ALTER FUNCTION public.get_accesslevels() OWNER TO evgenia;

--
-- TOC entry 260 (class 1255 OID 172084)
-- Name: get_alg_class_by_id(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_alg_class_by_id(idcl integer) RETURNS TABLE(name_algorithm_class character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "algorithm_class"."name_algorithm_class"
			    FROM "algorithm_class"
			    WHERE "algorithm_class"."id_algorithm_class" = idcl;
END
$$;


ALTER FUNCTION public.get_alg_class_by_id(idcl integer) OWNER TO evgenia;

--
-- TOC entry 235 (class 1255 OID 172039)
-- Name: get_algorithm_class(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_algorithm_class() RETURNS TABLE(id_algorithm_class integer, name_algorithm_class character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "algorithm_class"."id_algorithm_class",
			    "algorithm_class"."name_algorithm_class"
			    FROM "algorithm_class";
END
$$;


ALTER FUNCTION public.get_algorithm_class() OWNER TO evgenia;

--
-- TOC entry 246 (class 1255 OID 172067)
-- Name: get_all_methods(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_all_methods() RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    WHERE "method"."status_method" != 1 
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_all_methods() OWNER TO evgenia;

--
-- TOC entry 233 (class 1255 OID 172036)
-- Name: get_application_area(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_application_area() RETURNS TABLE(name_application_area character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "application_area"."name_application_area"
			    FROM "application_area";
END
$$;


ALTER FUNCTION public.get_application_area() OWNER TO evgenia;

--
-- TOC entry 261 (class 1255 OID 172085)
-- Name: get_complex_class_by_id(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_complex_class_by_id(idcl integer) RETURNS TABLE(name_complexity_class character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "complexity_class"."name_complexity_class"
			    FROM "complexity_class"
			    WHERE "complexity_class"."id_complexity_class" = idcl;
END
$$;


ALTER FUNCTION public.get_complex_class_by_id(idcl integer) OWNER TO evgenia;

--
-- TOC entry 234 (class 1255 OID 172038)
-- Name: get_complexity_class(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_complexity_class() RETURNS TABLE(id_complexity_class integer, name_complexity_class character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "complexity_class"."id_complexity_class",
			    "complexity_class"."name_complexity_class"
			    FROM "complexity_class";
END
$$;


ALTER FUNCTION public.get_complexity_class() OWNER TO evgenia;

--
-- TOC entry 264 (class 1255 OID 172091)
-- Name: get_constraint_by_id_meth(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_constraint_by_id_meth(idmethod integer) RETURNS TABLE(name_possib_constraint character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "possib_constraint"."name_possib_constraint"
			    FROM "possib_constraint"
			    JOIN "method_constraint"
			    ON "possib_constraint"."id_possib_constraint" = "method_constraint"."id_possib_constraint"
			    WHERE "method_constraint"."id_method" = idmethod;
END
$$;


ALTER FUNCTION public.get_constraint_by_id_meth(idmethod integer) OWNER TO evgenia;

--
-- TOC entry 266 (class 1255 OID 172094)
-- Name: get_constraints(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_constraints() RETURNS TABLE(id_possib_constraint integer, name_possib_constraint character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "possib_constraint"."id_possib_constraint",
			    "possib_constraint"."name_possib_constraint"
			    FROM "possib_constraint";
END
$$;


ALTER FUNCTION public.get_constraints() OWNER TO evgenia;

--
-- TOC entry 238 (class 1255 OID 172051)
-- Name: get_essence_change(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_essence_change() RETURNS TABLE(typname name, enumlabel name)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT t.typname, 
	                    e.enumlabel
			    FROM pg_type t, pg_enum e
			    WHERE t.oid = e.enumtypid AND t.typname = 'essence_change';
END
$$;


ALTER FUNCTION public.get_essence_change() OWNER TO evgenia;

--
-- TOC entry 288 (class 1255 OID 196610)
-- Name: get_lookbook(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_lookbook(namemethod character varying, nameuser character varying) RETURNS TABLE(date_change date, status_change essence_change, name_method character varying, name_user character varying, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "logbook_update"."date_change", 
			    "logbook_update"."status_change",
			    "method"."name_method", 
			    "users"."name_user", 
			    "access_levels"."name_access_level"
			    FROM "logbook_update"
			    JOIN "method"
			    ON "logbook_update"."id_method" = "method"."id_method"
			    JOIN "users"
			    ON "logbook_update"."id_user" = "users"."id_user"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "method"."name_method" ILIKE namemethod
			          AND "users"."name_user" ILIKE nameuser 
			    ORDER BY "logbook_update"."date_change" DESC;
END
$$;


ALTER FUNCTION public.get_lookbook(namemethod character varying, nameuser character varying) OWNER TO evgenia;

--
-- TOC entry 289 (class 1255 OID 196613)
-- Name: get_lookbook_f_date(character varying, character varying, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_lookbook_f_date(namemethod character varying, nameuser character varying, fdate date) RETURNS TABLE(date_change date, status_change essence_change, name_method character varying, name_user character varying, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "logbook_update"."date_change", 
			    "logbook_update"."status_change",
			    "method"."name_method", 
			    "users"."name_user", 
			    "access_levels"."name_access_level"
			    FROM "logbook_update"
			    JOIN "method"
			    ON "logbook_update"."id_method" = "method"."id_method"
			    JOIN "users"
			    ON "logbook_update"."id_user" = "users"."id_user"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "method"."name_method" ILIKE namemethod
			          AND "users"."name_user" ILIKE nameuser
			          AND "logbook_update"."date_change" >= fdate
			    ORDER BY "logbook_update"."date_change" DESC;
END
$$;


ALTER FUNCTION public.get_lookbook_f_date(namemethod character varying, nameuser character varying, fdate date) OWNER TO evgenia;

--
-- TOC entry 290 (class 1255 OID 196612)
-- Name: get_lookbook_l_date(character varying, character varying, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_lookbook_l_date(namemethod character varying, nameuser character varying, ldate date) RETURNS TABLE(date_change date, status_change essence_change, name_method character varying, name_user character varying, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "logbook_update"."date_change", 
			    "logbook_update"."status_change",
			    "method"."name_method", 
			    "users"."name_user", 
			    "access_levels"."name_access_level"
			    FROM "logbook_update"
			    JOIN "method"
			    ON "logbook_update"."id_method" = "method"."id_method"
			    JOIN "users"
			    ON "logbook_update"."id_user" = "users"."id_user"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "method"."name_method" ILIKE namemethod
			          AND "users"."name_user" ILIKE nameuser
			          AND "logbook_update"."date_change" <= ldate
			    ORDER BY "logbook_update"."date_change" DESC;
END
$$;


ALTER FUNCTION public.get_lookbook_l_date(namemethod character varying, nameuser character varying, ldate date) OWNER TO evgenia;

--
-- TOC entry 283 (class 1255 OID 196611)
-- Name: get_lookbook_two_date(character varying, character varying, date, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_lookbook_two_date(namemethod character varying, nameuser character varying, fdate date, ldate date) RETURNS TABLE(date_change date, status_change essence_change, name_method character varying, name_user character varying, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "logbook_update"."date_change", 
			    "logbook_update"."status_change",
			    "method"."name_method", 
			    "users"."name_user", 
			    "access_levels"."name_access_level"
			    FROM "logbook_update"
			    JOIN "method"
			    ON "logbook_update"."id_method" = "method"."id_method"
			    JOIN "users"
			    ON "logbook_update"."id_user" = "users"."id_user"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "method"."name_method" ILIKE namemethod
			          AND "users"."name_user" ILIKE nameuser
			          AND "logbook_update"."date_change" BETWEEN fdate AND ldate
			    ORDER BY "logbook_update"."date_change" DESC;
END
$$;


ALTER FUNCTION public.get_lookbook_two_date(namemethod character varying, nameuser character varying, fdate date, ldate date) OWNER TO evgenia;

--
-- TOC entry 244 (class 1255 OID 172070)
-- Name: get_methods_all_crit(character varying, integer, integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_all_crit(namemethod character varying, idtaskarea integer, idpracticaltask integer, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    JOIN "task_area"
			    ON "method_task_area"."id_task_area" = "task_area"."id_task_area"
			    JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    JOIN "practical_task"
			    ON "pract_task_area"."id_practical_task" = "practical_task"."id_practical_task"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND ("method_task_area"."id_task_area" = idtaskarea
			          OR "pract_task_area"."id_practical_task" = idpracticaltask)
			          AND "method"."id_algorithm_class" = idalgorithmclass
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_all_crit(namemethod character varying, idtaskarea integer, idpracticaltask integer, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 271 (class 1255 OID 172089)
-- Name: get_methods_by_id(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_by_id(idmethod integer) RETURNS TABLE(name_method character varying, numb_stages integer, value_memory character varying, description_stages text, simplified_code text, complexity_method character varying, id_algorithm_class integer, id_complexity_class integer, status_method integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."name_method",
	                    "method"."numb_stages",
			    "method"."value_memory",
			    "method"."description_stages",
			    "method"."simplified_code",
			    "method"."complexity_method",
			    "method"."id_algorithm_class",
			    "method"."id_complexity_class",
			    "method"."status_method"
			    FROM "method"
			    WHERE "method"."status_method" != 1 
			          AND "method"."id_method" = idmethod;
END
$$;


ALTER FUNCTION public.get_methods_by_id(idmethod integer) OWNER TO evgenia;

--
-- TOC entry 254 (class 1255 OID 172078)
-- Name: get_methods_crit_cla(character varying, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_cla(namemethod character varying, idalgorithmclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method"."id_algorithm_class" = idalgorithmclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_cla(namemethod character varying, idalgorithmclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 253 (class 1255 OID 172076)
-- Name: get_methods_crit_cla_clc(character varying, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_cla_clc(namemethod character varying, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method"."id_algorithm_class" = idalgorithmclass
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_cla_clc(namemethod character varying, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 255 (class 1255 OID 172079)
-- Name: get_methods_crit_clc(character varying, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_clc(namemethod character varying, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_clc(namemethod character varying, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 248 (class 1255 OID 172071)
-- Name: get_methods_crit_name_v(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_name_v(namemethod character varying, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_name_v(namemethod character varying, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 251 (class 1255 OID 172074)
-- Name: get_methods_crit_ptask(character varying, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_ptask(namemethod character varying, idpracticaltask integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    JOIN "task_area"
			    ON "method_task_area"."id_task_area" = "task_area"."id_task_area"
			    JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "pract_task_area"."id_practical_task" = idpracticaltask
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_ptask(namemethod character varying, idpracticaltask integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 256 (class 1255 OID 172080)
-- Name: get_methods_crit_ptask_cla(character varying, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_ptask_cla(namemethod character varying, idpracticaltask integer, idalgorithmclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    JOIN "task_area"
			    ON "method_task_area"."id_task_area" = "task_area"."id_task_area"
			    JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "pract_task_area"."id_practical_task" = idpracticaltask
			          AND "method"."id_algorithm_class" = idalgorithmclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_ptask_cla(namemethod character varying, idpracticaltask integer, idalgorithmclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 250 (class 1255 OID 172073)
-- Name: get_methods_crit_ptask_cla_clc(character varying, integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_ptask_cla_clc(namemethod character varying, idpracticaltask integer, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    JOIN "task_area"
			    ON "method_task_area"."id_task_area" = "task_area"."id_task_area"
			    JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "pract_task_area"."id_practical_task" = idpracticaltask
			          AND "method"."id_algorithm_class" = idalgorithmclass
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_ptask_cla_clc(namemethod character varying, idpracticaltask integer, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 257 (class 1255 OID 172081)
-- Name: get_methods_crit_ptask_clc(character varying, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_ptask_clc(namemethod character varying, idpracticaltask integer, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    JOIN "task_area"
			    ON "method_task_area"."id_task_area" = "task_area"."id_task_area"
			    JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "pract_task_area"."id_practical_task" = idpracticaltask
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_ptask_clc(namemethod character varying, idpracticaltask integer, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 252 (class 1255 OID 172075)
-- Name: get_methods_crit_tarea(character varying, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_tarea(namemethod character varying, idtaskarea integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method_task_area"."id_task_area" = idtaskarea
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_tarea(namemethod character varying, idtaskarea integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 258 (class 1255 OID 172082)
-- Name: get_methods_crit_tarea_cla(character varying, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_tarea_cla(namemethod character varying, idtaskarea integer, idalgorithmclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method_task_area"."id_task_area" = idtaskarea
			          AND "method"."id_algorithm_class" = idalgorithmclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_tarea_cla(namemethod character varying, idtaskarea integer, idalgorithmclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 249 (class 1255 OID 172072)
-- Name: get_methods_crit_tarea_cla_clc(character varying, integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_tarea_cla_clc(namemethod character varying, idtaskarea integer, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method_task_area"."id_task_area" = idtaskarea
			          AND "method"."id_algorithm_class" = idalgorithmclass
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_tarea_cla_clc(namemethod character varying, idtaskarea integer, idalgorithmclass integer, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 259 (class 1255 OID 172083)
-- Name: get_methods_crit_tarea_clc(character varying, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_methods_crit_tarea_clc(namemethod character varying, idtaskarea integer, idcomplexityclass integer, valuememory character varying) RETURNS TABLE(id_method integer, name_method character varying, name_algorithm_class character varying, name_complexity_class character varying, complexity_method character varying, value_memory character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method"."id_method", 
			    "method"."name_method",
			    "algorithm_class"."name_algorithm_class", 
			    "complexity_class"."name_complexity_class", 
			    "method"."complexity_method",
			    "method"."value_memory"
			    FROM "method"
			    JOIN "algorithm_class"
			    ON "method"."id_algorithm_class" = "algorithm_class"."id_algorithm_class"
			    JOIN "complexity_class"
			    ON "method"."id_complexity_class" = "complexity_class"."id_complexity_class"
			    JOIN "method_task_area"
			    ON "method"."id_method" = "method_task_area"."id_method"
			    WHERE "method"."status_method" != 1 
			          AND "method"."name_method" ILIKE namemethod
			          AND "method"."value_memory" ILIKE valuememory 
			          AND "method_task_area"."id_task_area" = idtaskarea
			          AND "method"."id_complexity_class" = idcomplexityclass
			    ORDER BY "method"."name_method";
END
$$;


ALTER FUNCTION public.get_methods_crit_tarea_clc(namemethod character varying, idtaskarea integer, idcomplexityclass integer, valuememory character varying) OWNER TO evgenia;

--
-- TOC entry 236 (class 1255 OID 172042)
-- Name: get_practical_task(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_practical_task(nametype character varying) RETURNS TABLE(id_practical_task integer, name_application_area character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "practical_task"."id_practical_task",
			    "practical_task"."name_practical_task"
			    FROM "practical_task"
			    JOIN "application_area"
			    ON "practical_task"."id_application_area" = "application_area"."id_application_area"
			    WHERE "application_area"."name_application_area" = nametype;
END
$$;


ALTER FUNCTION public.get_practical_task(nametype character varying) OWNER TO evgenia;

--
-- TOC entry 237 (class 1255 OID 172043)
-- Name: get_task_area(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_task_area(nametype character varying) RETURNS TABLE(id_task_area integer, name_task_area character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "task_area"."id_task_area",
			    "task_area"."name_task_area"
			    FROM "task_area"
			    JOIN "type_task_area"
			    ON "task_area"."id_type_task_area" = "type_task_area"."id_type_task_area"
			    WHERE "type_task_area"."name_type_task_area" = nametype;
END
$$;


ALTER FUNCTION public.get_task_area(nametype character varying) OWNER TO evgenia;

--
-- TOC entry 272 (class 1255 OID 180228)
-- Name: get_task_area_by_id_meth(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_task_area_by_id_meth(idmeth integer) RETURNS TABLE(id_type_task_area integer, name_type_task_area character varying, id_task_area integer, name_task_area character varying, id_application_area integer, name_application_area character varying, id_practical_task integer, name_practical_task character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "task_area"."id_type_task_area",
	                    "type_task_area"."name_type_task_area",
			    "task_area"."id_task_area",
			    "task_area"."name_task_area",
			    "practical_task"."id_application_area",
			    "application_area"."name_application_area",
			    "practical_task"."id_practical_task",
			    "practical_task"."name_practical_task"
			    FROM "task_area"
			    JOIN "type_task_area"
			    ON "task_area"."id_type_task_area" = "type_task_area"."id_type_task_area"
			    JOIN "method_task_area"
			    ON "task_area"."id_task_area" = "method_task_area"."id_task_area"
			    JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    JOIN "practical_task"
			    ON "pract_task_area"."id_practical_task" = "practical_task"."id_practical_task"
			    JOIN "application_area"
			    ON "practical_task"."id_application_area" = "application_area"."id_application_area"
			    WHERE "method_task_area"."id_method" = idmeth;
END
$$;


ALTER FUNCTION public.get_task_area_by_id_meth(idmeth integer) OWNER TO evgenia;

--
-- TOC entry 291 (class 1255 OID 196615)
-- Name: get_tasks_method_by_id(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_tasks_method_by_id(idmethod integer) RETURNS TABLE(id_task_area integer, name_type_task_area character varying, name_task_area character varying, name_application_area character varying, name_practical_task character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "method_task_area"."id_task_area", 
			    "type_task_area"."name_type_task_area",
			    "task_area"."name_task_area", 
			    "application_area"."name_application_area", 
			    "practical_task"."name_practical_task"
			    FROM "method_task_area"
			    FULL OUTER JOIN "task_area"
			    ON "method_task_area"."id_task_area" = "task_area"."id_task_area"
			    FULL OUTER JOIN "type_task_area"
			    ON "type_task_area"."id_type_task_area" = "task_area"."id_type_task_area"
			    FULL OUTER JOIN "pract_task_area"
			    ON "task_area"."id_task_area" = "pract_task_area"."id_task_area"
			    FULL OUTER JOIN "practical_task"
			    ON "pract_task_area"."id_practical_task" = "practical_task"."id_practical_task"
			    FULL OUTER JOIN "application_area"
			    ON "practical_task"."id_application_area" = "application_area"."id_application_area"
			    WHERE "method_task_area"."id_method" = idmethod 
			    ORDER BY "type_task_area"."name_type_task_area";
END
$$;


ALTER FUNCTION public.get_tasks_method_by_id(idmethod integer) OWNER TO evgenia;

--
-- TOC entry 265 (class 1255 OID 172092)
-- Name: get_theorems(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_theorems() RETURNS TABLE(id_theorem integer, name_theorem character varying, statement_theorem text, name_resource character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "theorem"."id_theorem",
	                    "theorem"."name_theorem",
			    "theorem"."statement_theorem",
			    "theorem"."name_resource"
			    FROM "theorem";
END
$$;


ALTER FUNCTION public.get_theorems() OWNER TO evgenia;

--
-- TOC entry 263 (class 1255 OID 172090)
-- Name: get_theorems_by_id_meth(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_theorems_by_id_meth(idmethod integer) RETURNS TABLE(id_theorem integer, name_theorem character varying, statement_theorem text, name_resource character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "theorem"."id_theorem",
	                    "theorem"."name_theorem",
			    "theorem"."statement_theorem",
			    "theorem"."name_resource"
			    FROM "theorem"
			    JOIN "method_theorem"
			    ON "theorem"."id_theorem" = "method_theorem"."id_theorem"
			    WHERE "method_theorem"."id_method" = idmethod;
END
$$;


ALTER FUNCTION public.get_theorems_by_id_meth(idmethod integer) OWNER TO evgenia;

--
-- TOC entry 270 (class 1255 OID 180225)
-- Name: get_theorems_by_id_theorem(integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_theorems_by_id_theorem(idtheor integer) RETURNS TABLE(statement_theorem text, name_resource character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "theorem"."statement_theorem",
			    "theorem"."name_resource"
			    FROM "theorem"
			    WHERE "theorem"."id_theorem" = idtheor;
END
$$;


ALTER FUNCTION public.get_theorems_by_id_theorem(idtheor integer) OWNER TO evgenia;

--
-- TOC entry 232 (class 1255 OID 172035)
-- Name: get_type_task_area(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_type_task_area() RETURNS TABLE(type_task_area character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "type_task_area"."name_type_task_area"
			    FROM "type_task_area";
END
$$;


ALTER FUNCTION public.get_type_task_area() OWNER TO evgenia;

--
-- TOC entry 273 (class 1255 OID 188417)
-- Name: get_users(); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_users() RETURNS TABLE(id_user integer, id_access_level integer, login character varying, name_user character varying, status_account integer, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "users"."id_user", 
			    "users"."id_access_level",
			    "users"."login", 
			    "users"."name_user", 
			    "users"."status_account",
			    "access_levels"."name_access_level"
			    FROM "users"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "users"."status_account" = 0 
			    ORDER BY "users"."id_access_level";
END
$$;


ALTER FUNCTION public.get_users() OWNER TO evgenia;

--
-- TOC entry 275 (class 1255 OID 180229)
-- Name: get_users_by_name(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_users_by_name(nuser character varying) RETURNS TABLE(id_user integer, id_access_level integer, login character varying, name_user character varying, status_account integer, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "users"."id_user", 
			    "users"."id_access_level",
			    "users"."login", 
			    "users"."name_user", 
			    "users"."status_account",
			    "access_levels"."name_access_level"
			    FROM "users"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "users"."name_user" ILIKE nuser
			    ORDER BY "users"."id_access_level";
END
$$;


ALTER FUNCTION public.get_users_by_name(nuser character varying) OWNER TO evgenia;

--
-- TOC entry 276 (class 1255 OID 180230)
-- Name: get_users_by_name_level(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION get_users_by_name_level(nuser character varying, nlevel character varying) RETURNS TABLE(id_user integer, id_access_level integer, login character varying, name_user character varying, status_account integer, name_access_level character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY SELECT "users"."id_user", 
			    "users"."id_access_level",
			    "users"."login", 
			    "users"."name_user", 
			    "users"."status_account",
			    "access_levels"."name_access_level"
			    FROM "users"
			    JOIN "access_levels"
			    ON "users"."id_access_level" = "access_levels"."id_access_level"
			    WHERE "users"."name_user" ILIKE nuser
			    AND "access_levels"."name_access_level" ILIKE nlevel
			    ORDER BY "users"."id_access_level";
END
$$;


ALTER FUNCTION public.get_users_by_name_level(nuser character varying, nlevel character varying) OWNER TO evgenia;

--
-- TOC entry 215 (class 1255 OID 155649)
-- Name: new_accesslevel(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_accesslevel(nameaccesslevel character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	accesslevelcount integer;
BEGIN
	SELECT COUNT(*) INTO accesslevelcount FROM "access_levels" WHERE "name_access_level" =nameaccesslevel;
	IF (accesslevelcount=0)
	THEN
	INSERT INTO "access_levels" (id_access_level,name_access_level)
	VALUES (DEFAULT,nameaccesslevel)
	RETURNING id_access_level INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_accesslevel(nameaccesslevel character varying) OWNER TO evgenia;

--
-- TOC entry 218 (class 1255 OID 155657)
-- Name: new_algorithm_class(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_algorithm_class(nameclass character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	classcount integer;
BEGIN
	SELECT COUNT(*) INTO classcount FROM "algorithm_class" WHERE "name_algorithm_class" =nameclass;
	IF (classcount=0)
	THEN
	INSERT INTO "algorithm_class" (id_algorithm_class,name_algorithm_class)
	VALUES (DEFAULT,nameclass)
	RETURNING id_algorithm_class INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_algorithm_class(nameclass character varying) OWNER TO evgenia;

--
-- TOC entry 222 (class 1255 OID 155662)
-- Name: new_application_area(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_application_area(namenew character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "application_area" WHERE "name_application_area" =namenew;
	IF (entrycount=0)
	THEN
	INSERT INTO "application_area" (id_application_area,name_application_area)
	VALUES (DEFAULT,namenew)
	RETURNING id_application_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_application_area(namenew character varying) OWNER TO evgenia;

--
-- TOC entry 219 (class 1255 OID 155658)
-- Name: new_complexity_class(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_complexity_class(nameclass character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	classcount integer;
BEGIN
	SELECT COUNT(*) INTO classcount FROM "complexity_class" WHERE "name_complexity_class" =nameclass;
	IF (classcount=0)
	THEN
	INSERT INTO "complexity_class" (id_complexity_class,name_complexity_class)
	VALUES (DEFAULT,nameclass)
	RETURNING id_complexity_class INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_complexity_class(nameclass character varying) OWNER TO evgenia;

--
-- TOC entry 239 (class 1255 OID 172052)
-- Name: new_logbook_update(integer, integer, essence_change, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_logbook_update(idmeth integer, iduser integer, statch essence_change, datech date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	INSERT INTO "logbook_update" (id_logbook_update,id_method,id_user,status_change,date_change)
	VALUES (DEFAULT,idmeth,iduser,statch,datech)
	RETURNING id_logbook_update INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.new_logbook_update(idmeth integer, iduser integer, statch essence_change, datech date) OWNER TO evgenia;

--
-- TOC entry 245 (class 1255 OID 172056)
-- Name: new_method(character varying, integer, character varying, text, text, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method(namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idalgorithmcl INTEGER DEFAULT (SELECT "id_algorithm_class" FROM "algorithm_class" WHERE "name_algorithm_class"=namealgorithmcl);
	idcomplexitycl INTEGER DEFAULT (SELECT "id_complexity_class" FROM "complexity_class" WHERE "name_complexity_class"=namecomplexitycl);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method" WHERE "name_method" =namemethod AND "status_method"=0;
	IF (entrycount=0)
	THEN
	INSERT INTO "method" (id_method,name_method,numb_stages,value_memory,description_stages,simplified_code,complexity_method,id_algorithm_class,id_complexity_class,status_method)
	VALUES (DEFAULT,namemethod,numbstages,valuemem,descriptionstages,simplifiedcode,complexitymethod,idalgorithmcl,idcomplexitycl,0)
	RETURNING id_method INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method(namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying) OWNER TO evgenia;

--
-- TOC entry 241 (class 1255 OID 172054)
-- Name: new_method_constraint(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_constraint(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method_constraint" WHERE "id_method" =idfirst AND "id_possib_constraint" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "method_constraint" (id_method_constraint,id_method,id_possib_constraint)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_method_constraint INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_constraint(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 225 (class 1255 OID 155667)
-- Name: new_method_constraint(integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_constraint(idfirst integer, namesecond character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idsecond INTEGER DEFAULT (SELECT "id_possib_constraint" FROM "possib_constraint" WHERE "name_possib_constraint"=namesecond);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method_constraint" WHERE "id_method" =idfirst AND "id_possib_constraint" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "method_constraint" (id_method_constraint,id_method,id_possib_constraint)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_method_constraint INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_constraint(idfirst integer, namesecond character varying) OWNER TO evgenia;

--
-- TOC entry 247 (class 1255 OID 172065)
-- Name: new_method_logbook(character varying, integer, character varying, text, text, character varying, character varying, character varying, integer, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_logbook(namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying, iduser integer, datech date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	idmethod INTEGER;
	idlogbook INTEGER;
BEGIN
	idmethod = (SELECT * FROM new_method(namemethod,numbstages,valuemem,descriptionstages,simplifiedcode,complexitymethod,namealgorithmcl,namecomplexitycl));
	IF (idmethod != -2) THEN
		idlogbook = (SELECT * FROM new_logbook_update(idmethod, iduser, 'Добавление', datech));
		result = idmethod;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_logbook(namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying, iduser integer, datech date) OWNER TO evgenia;

--
-- TOC entry 242 (class 1255 OID 172055)
-- Name: new_method_task_area(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_task_area(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method_task_area" WHERE "id_method" =idfirst AND "id_task_area" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "method_task_area"(id_method_task_area,id_method,id_task_area)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_method_task_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_task_area(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 227 (class 1255 OID 155669)
-- Name: new_method_task_area(integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_task_area(idfirst integer, namesecond character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idsecond INTEGER DEFAULT (SELECT "id_task_area" FROM "task_area" WHERE "name_task_area"=namesecond);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method_task_area" WHERE "id_method" =idfirst AND "id_task_area" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "method_task_area"(id_method_task_area,id_method,id_task_area)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_method_task_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_task_area(idfirst integer, namesecond character varying) OWNER TO evgenia;

--
-- TOC entry 240 (class 1255 OID 172053)
-- Name: new_method_theorem(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_theorem(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method_theorem" WHERE "id_method" =idfirst AND "id_theorem" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "method_theorem" (id_method_theorem,id_method,id_theorem)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_method_theorem INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_theorem(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 226 (class 1255 OID 155668)
-- Name: new_method_theorem(integer, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_method_theorem(idfirst integer, namesecond character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idsecond INTEGER DEFAULT (SELECT "id_theorem" FROM "theorem" WHERE "name_theorem"=namesecond);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "method_theorem" WHERE "id_method" =idfirst AND "id_theorem" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "method_theorem" (id_method_theorem,id_method,id_theorem)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_method_theorem INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_method_theorem(idfirst integer, namesecond character varying) OWNER TO evgenia;

--
-- TOC entry 221 (class 1255 OID 155659)
-- Name: new_possib_constraint(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_possib_constraint(namepossibconstraint character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	constraintcount integer;
BEGIN
	SELECT COUNT(*) INTO constraintcount FROM "possib_constraint" WHERE "name_possib_constraint" =namepossibconstraint;
	IF (constraintcount=0)
	THEN
	INSERT INTO "possib_constraint" (id_possib_constraint,name_possib_constraint)
	VALUES (DEFAULT,namepossibconstraint)
	RETURNING id_possib_constraint INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_possib_constraint(namepossibconstraint character varying) OWNER TO evgenia;

--
-- TOC entry 277 (class 1255 OID 196614)
-- Name: new_pract_task_area(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_pract_task_area(idfirst integer, idsecond integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "pract_task_area" WHERE "id_task_area" =idfirst AND "id_practical_task" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "pract_task_area" (id_pract_task_area,id_task_area,id_practical_task)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_pract_task_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_pract_task_area(idfirst integer, idsecond integer) OWNER TO evgenia;

--
-- TOC entry 223 (class 1255 OID 155664)
-- Name: new_pract_task_area(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_pract_task_area(namefirst character varying, namesecond character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idfirst INTEGER DEFAULT (SELECT "id_task_area" FROM "task_area" WHERE "name_task_area"=namefirst);
	idsecond INTEGER DEFAULT (SELECT "id_practical_task" FROM "practical_task" WHERE "name_practical_task"=namesecond);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "pract_task_area" WHERE "id_task_area" =idfirst AND "id_practical_task" =idsecond;
	IF (entrycount=0)
	THEN
	INSERT INTO "pract_task_area" (id_pract_task_area,id_task_area,id_practical_task)
	VALUES (DEFAULT,idfirst,idsecond)
	RETURNING id_pract_task_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_pract_task_area(namefirst character varying, namesecond character varying) OWNER TO evgenia;

--
-- TOC entry 230 (class 1255 OID 172033)
-- Name: new_practical_task(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_practical_task(nametype character varying, namenew character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idtype INTEGER DEFAULT (SELECT "id_application_area" FROM "application_area" WHERE "name_application_area"=nametype);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "practical_task" WHERE "name_practical_task" =namenew;
	IF (entrycount=0)
	THEN
	INSERT INTO "practical_task" (id_practical_task,id_application_area,name_practical_task)
	VALUES (DEFAULT,idtype,namenew)
	RETURNING id_practical_task INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_practical_task(nametype character varying, namenew character varying) OWNER TO evgenia;

--
-- TOC entry 231 (class 1255 OID 172034)
-- Name: new_task_area(character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_task_area(nametype character varying, namenew character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
	idtype INTEGER DEFAULT (SELECT "id_type_task_area" FROM "type_task_area" WHERE "name_type_task_area"=nametype);
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "task_area" WHERE "name_task_area" =namenew;
	IF (entrycount=0)
	THEN
	INSERT INTO "task_area" (id_task_area,id_type_task_area,name_task_area)
	VALUES (DEFAULT,idtype,namenew)
	RETURNING id_task_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_task_area(nametype character varying, namenew character varying) OWNER TO evgenia;

--
-- TOC entry 224 (class 1255 OID 155665)
-- Name: new_theorem(character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_theorem(nametheorem character varying, statementtheorem character varying, nameresource character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "theorem" WHERE "name_theorem" =nametheorem;
	IF (entrycount=0)
	THEN
	INSERT INTO "theorem" (id_theorem,name_theorem,statement_theorem,name_resource)
	VALUES (DEFAULT,nametheorem,statementtheorem,nameresource)
	RETURNING id_theorem INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_theorem(nametheorem character varying, statementtheorem character varying, nameresource character varying) OWNER TO evgenia;

--
-- TOC entry 220 (class 1255 OID 155660)
-- Name: new_type_task_area(character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_type_task_area(namenew character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	entrycount integer;
BEGIN
	SELECT COUNT(*) INTO entrycount FROM "type_task_area" WHERE "name_type_task_area" =namenew;
	IF (entrycount=0)
	THEN
	INSERT INTO "type_task_area" (id_type_task_area,name_type_task_area)
	VALUES (DEFAULT,namenew)
	RETURNING id_type_task_area INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_type_task_area(namenew character varying) OWNER TO evgenia;

--
-- TOC entry 228 (class 1255 OID 163875)
-- Name: new_user(character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION new_user(nameaccesslevel character varying, userlogin character varying, userpassword character varying, username character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	usercount integer;
	idaccesslevel INTEGER DEFAULT (SELECT "id_access_level" FROM "access_levels" WHERE "name_access_level"=nameaccesslevel);
BEGIN
	SELECT COUNT(*) INTO usercount FROM "users" WHERE "login" =userlogin;
	IF (usercount=0)
	THEN
	INSERT INTO "users" (id_user,id_access_level,login,password,name_user,status_account)
	VALUES (DEFAULT,idaccesslevel,userlogin,userpassword,username,0)
	RETURNING id_user INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.new_user(nameaccesslevel character varying, userlogin character varying, userpassword character varying, username character varying) OWNER TO evgenia;

--
-- TOC entry 285 (class 1255 OID 196628)
-- Name: update_method(integer, character varying, integer, character varying, text, text, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_method(idmeth integer, namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	usercount integer;
	idalgorithmcl INTEGER DEFAULT (SELECT "id_algorithm_class" FROM "algorithm_class" WHERE "name_algorithm_class"=namealgorithmcl);
	idcomplexitycl INTEGER DEFAULT (SELECT "id_complexity_class" FROM "complexity_class" WHERE "name_complexity_class"=namecomplexitycl);
BEGIN
	UPDATE "method" 
	SET "name_method" =namemethod, "numb_stages" =numbstages, 
	"value_memory" =valuemem, "description_stages" =descriptionstages, 
	"simplified_code"=simplifiedcode, "complexity_method" =complexitymethod,
	"id_algorithm_class" =idalgorithmcl, "id_complexity_class" =idcomplexitycl
	WHERE "id_method" =idmeth
	RETURNING id_method INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.update_method(idmeth integer, namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying) OWNER TO evgenia;

--
-- TOC entry 269 (class 1255 OID 172098)
-- Name: update_method_code(integer, text); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_method_code(idmeth integer, discrcode text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
BEGIN
	UPDATE "method" 
	SET "simplified_code" =discrcode
	WHERE "id_method" =idmeth
	RETURNING id_method INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.update_method_code(idmeth integer, discrcode text) OWNER TO evgenia;

--
-- TOC entry 284 (class 1255 OID 196629)
-- Name: update_method_logbook(integer, character varying, integer, character varying, text, text, character varying, character varying, character varying, integer, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_method_logbook(idmeth integer, namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying, iduser integer, datech date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	idmethod INTEGER;
	idlogbook INTEGER;
BEGIN
	idmethod = (SELECT * FROM update_method(idmeth,namemethod,numbstages,valuemem,descriptionstages,simplifiedcode,complexitymethod,namealgorithmcl,namecomplexitycl));
	IF (idmethod != -2) THEN
		idlogbook = (SELECT * FROM new_logbook_update(idmethod, iduser, 'Изменение', datech));
		result = idlogbook;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.update_method_logbook(idmeth integer, namemethod character varying, numbstages integer, valuemem character varying, descriptionstages text, simplifiedcode text, complexitymethod character varying, namealgorithmcl character varying, namecomplexitycl character varying, iduser integer, datech date) OWNER TO evgenia;

--
-- TOC entry 286 (class 1255 OID 196630)
-- Name: update_method_logbook_simp(integer, integer, date); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_method_logbook_simp(idmeth integer, iduser integer, datech date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	idmethod INTEGER;
	idlogbook INTEGER;
BEGIN
	idlogbook = (SELECT * FROM new_logbook_update(idmethod, iduser, 'Изменение', datech));
	result = idlogbook;
	RETURN result;
END
$$;


ALTER FUNCTION public.update_method_logbook_simp(idmeth integer, iduser integer, datech date) OWNER TO evgenia;

--
-- TOC entry 268 (class 1255 OID 172097)
-- Name: update_method_stages(integer, text); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_method_stages(idmeth integer, discrstages text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
BEGIN
	UPDATE "method" 
	SET "description_stages" =discrstages
	WHERE "id_method" =idmeth
	RETURNING id_method INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.update_method_stages(idmeth integer, discrstages text) OWNER TO evgenia;

--
-- TOC entry 280 (class 1255 OID 196621)
-- Name: update_method_status(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_method_status(idmeth integer, statmeth integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
BEGIN
	UPDATE "method" 
	SET "status_method" =statmeth
	WHERE "id_method" =idmeth
	RETURNING id_method INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.update_method_status(idmeth integer, statmeth integer) OWNER TO evgenia;

--
-- TOC entry 267 (class 1255 OID 172096)
-- Name: update_theorem(integer, text); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_theorem(idtheorem integer, statementtheorem text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
BEGIN
	UPDATE "theorem" 
	SET "statement_theorem" =statementtheorem
	WHERE "id_theorem" =idtheorem
	RETURNING id_theorem INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.update_theorem(idtheorem integer, statementtheorem text) OWNER TO evgenia;

--
-- TOC entry 216 (class 1255 OID 155654)
-- Name: update_user_info(integer, integer, character varying, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_user_info(iduser integer, idaccesslevel integer, userlogin character varying, userpassword character varying, username character varying, statacc integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	usercount integer;
BEGIN
	SELECT COUNT(*) INTO usercount FROM "users" WHERE "login" =userlogin AND "id_user" !=iduser AND "status_account"=0;
	IF (usercount=0)
	THEN
	UPDATE "users" 
	SET "id_access_level" =idaccesslevel, "login" =userlogin, "password" =userpassword, "name_user" =username, "status_account"=statacc
	WHERE "id_user" =iduser
	RETURNING id_user INTO result;
	ELSE
	result=-2; 
	END IF;
	RETURN result;
END
$$;


ALTER FUNCTION public.update_user_info(iduser integer, idaccesslevel integer, userlogin character varying, userpassword character varying, username character varying, statacc integer) OWNER TO evgenia;

--
-- TOC entry 262 (class 1255 OID 196609)
-- Name: update_user_status(integer, integer); Type: FUNCTION; Schema: public; Owner: evgenia
--

CREATE FUNCTION update_user_status(iduser integer, statacc integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
	result INTEGER;
	usercount integer;
BEGIN
	
	UPDATE "users" 
	SET "status_account"=statacc
	WHERE "id_user" =iduser
	RETURNING id_user INTO result;

	RETURN result;
END
$$;


ALTER FUNCTION public.update_user_status(iduser integer, statacc integer) OWNER TO evgenia;

--
-- TOC entry 174 (class 1259 OID 139276)
-- Name: access_level_id_access_level_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE access_level_id_access_level_seq
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE access_level_id_access_level_seq OWNER TO evgenia;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 176 (class 1259 OID 139280)
-- Name: access_levels; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE access_levels (
    id_access_level integer DEFAULT nextval('access_level_id_access_level_seq'::regclass) NOT NULL,
    name_access_level character varying
);


ALTER TABLE access_levels OWNER TO evgenia;

--
-- TOC entry 180 (class 1259 OID 147459)
-- Name: algorithm_class_id_algorithm_class_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE algorithm_class_id_algorithm_class_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE algorithm_class_id_algorithm_class_seq OWNER TO evgenia;

--
-- TOC entry 182 (class 1259 OID 147469)
-- Name: algorithm_class; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE algorithm_class (
    id_algorithm_class integer DEFAULT nextval('algorithm_class_id_algorithm_class_seq'::regclass) NOT NULL,
    name_algorithm_class character varying(30)
);


ALTER TABLE algorithm_class OWNER TO evgenia;

--
-- TOC entry 185 (class 1259 OID 147502)
-- Name: application_area_id_application_area_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE application_area_id_application_area_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE application_area_id_application_area_seq OWNER TO evgenia;

--
-- TOC entry 186 (class 1259 OID 147504)
-- Name: application_area; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE application_area (
    id_application_area integer DEFAULT nextval('application_area_id_application_area_seq'::regclass) NOT NULL,
    name_application_area character varying(50)
);


ALTER TABLE application_area OWNER TO evgenia;

--
-- TOC entry 179 (class 1259 OID 147457)
-- Name: complexity_class_id_complexity_class_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE complexity_class_id_complexity_class_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE complexity_class_id_complexity_class_seq OWNER TO evgenia;

--
-- TOC entry 181 (class 1259 OID 147463)
-- Name: complexity_class; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE complexity_class (
    id_complexity_class integer DEFAULT nextval('complexity_class_id_complexity_class_seq'::regclass) NOT NULL,
    name_complexity_class character varying(30)
);


ALTER TABLE complexity_class OWNER TO evgenia;

--
-- TOC entry 201 (class 1259 OID 163856)
-- Name: logbook_update_id_logbook_update_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE logbook_update_id_logbook_update_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE logbook_update_id_logbook_update_seq OWNER TO evgenia;

--
-- TOC entry 202 (class 1259 OID 163858)
-- Name: logbook_update; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE logbook_update (
    id_logbook_update integer DEFAULT nextval('logbook_update_id_logbook_update_seq'::regclass) NOT NULL,
    id_method integer,
    id_user integer,
    status_change essence_change,
    date_change date
);


ALTER TABLE logbook_update OWNER TO evgenia;

--
-- TOC entry 191 (class 1259 OID 147541)
-- Name: method_id_method_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE method_id_method_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE method_id_method_seq OWNER TO evgenia;

--
-- TOC entry 192 (class 1259 OID 147543)
-- Name: method; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE method (
    id_method integer DEFAULT nextval('method_id_method_seq'::regclass) NOT NULL,
    name_method character varying(100),
    numb_stages integer,
    value_memory character varying(50),
    description_stages text,
    simplified_code text,
    complexity_method character varying(100),
    id_algorithm_class integer,
    id_complexity_class integer,
    status_method integer
);


ALTER TABLE method OWNER TO evgenia;

--
-- TOC entry 199 (class 1259 OID 147604)
-- Name: method_constraint_id_method_constraint; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE method_constraint_id_method_constraint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE method_constraint_id_method_constraint OWNER TO evgenia;

--
-- TOC entry 200 (class 1259 OID 147606)
-- Name: method_constraint; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE method_constraint (
    id_method_constraint integer DEFAULT nextval('method_constraint_id_method_constraint'::regclass) NOT NULL,
    id_method integer,
    id_possib_constraint integer
);


ALTER TABLE method_constraint OWNER TO evgenia;

--
-- TOC entry 195 (class 1259 OID 147577)
-- Name: method_task_area_id_method_task_area; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE method_task_area_id_method_task_area
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE method_task_area_id_method_task_area OWNER TO evgenia;

--
-- TOC entry 196 (class 1259 OID 147579)
-- Name: method_task_area; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE method_task_area (
    id_method_task_area integer DEFAULT nextval('method_task_area_id_method_task_area'::regclass) NOT NULL,
    id_method integer,
    id_task_area integer
);


ALTER TABLE method_task_area OWNER TO evgenia;

--
-- TOC entry 193 (class 1259 OID 147557)
-- Name: method_theorem_id_method_theorem; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE method_theorem_id_method_theorem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE method_theorem_id_method_theorem OWNER TO evgenia;

--
-- TOC entry 194 (class 1259 OID 147559)
-- Name: method_theorem; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE method_theorem (
    id_method_theorem integer DEFAULT nextval('method_theorem_id_method_theorem'::regclass) NOT NULL,
    id_method integer,
    id_theorem integer
);


ALTER TABLE method_theorem OWNER TO evgenia;

--
-- TOC entry 197 (class 1259 OID 147596)
-- Name: possib_constraint_id_possib_constraint; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE possib_constraint_id_possib_constraint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE possib_constraint_id_possib_constraint OWNER TO evgenia;

--
-- TOC entry 198 (class 1259 OID 147598)
-- Name: possib_constraint; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE possib_constraint (
    id_possib_constraint integer DEFAULT nextval('possib_constraint_id_possib_constraint'::regclass) NOT NULL,
    name_possib_constraint character varying(200)
);


ALTER TABLE possib_constraint OWNER TO evgenia;

--
-- TOC entry 189 (class 1259 OID 147523)
-- Name: pract_task_area_id_pract_task_area_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE pract_task_area_id_pract_task_area_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE pract_task_area_id_pract_task_area_seq OWNER TO evgenia;

--
-- TOC entry 190 (class 1259 OID 147525)
-- Name: pract_task_area; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE pract_task_area (
    id_pract_task_area integer DEFAULT nextval('pract_task_area_id_pract_task_area_seq'::regclass) NOT NULL,
    id_task_area integer,
    id_practical_task integer
);


ALTER TABLE pract_task_area OWNER TO evgenia;

--
-- TOC entry 187 (class 1259 OID 147510)
-- Name: practical_task_id_practical_task_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE practical_task_id_practical_task_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE practical_task_id_practical_task_seq OWNER TO evgenia;

--
-- TOC entry 188 (class 1259 OID 147512)
-- Name: practical_task; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE practical_task (
    id_practical_task integer DEFAULT nextval('practical_task_id_practical_task_seq'::regclass) NOT NULL,
    id_application_area integer,
    name_practical_task character varying(50)
);


ALTER TABLE practical_task OWNER TO evgenia;

--
-- TOC entry 173 (class 1259 OID 139274)
-- Name: task_area_id_task_area_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE task_area_id_task_area_seq
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE task_area_id_task_area_seq OWNER TO evgenia;

--
-- TOC entry 178 (class 1259 OID 139300)
-- Name: task_area; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE task_area (
    id_task_area integer DEFAULT nextval('task_area_id_task_area_seq'::regclass) NOT NULL,
    id_type_task_area integer,
    name_task_area character varying(100)
);


ALTER TABLE task_area OWNER TO evgenia;

--
-- TOC entry 183 (class 1259 OID 147491)
-- Name: theorem_id_theorem_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE theorem_id_theorem_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE theorem_id_theorem_seq OWNER TO evgenia;

--
-- TOC entry 184 (class 1259 OID 147493)
-- Name: theorem; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE theorem (
    id_theorem integer DEFAULT nextval('theorem_id_theorem_seq'::regclass) NOT NULL,
    name_theorem character varying(150),
    statement_theorem text,
    name_resource character varying(300)
);


ALTER TABLE theorem OWNER TO evgenia;

--
-- TOC entry 171 (class 1259 OID 139266)
-- Name: type_task_area_id_type_task_area_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE type_task_area_id_type_task_area_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE type_task_area_id_type_task_area_seq OWNER TO evgenia;

--
-- TOC entry 172 (class 1259 OID 139268)
-- Name: type_task_area; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE type_task_area (
    id_type_task_area integer DEFAULT nextval('type_task_area_id_type_task_area_seq'::regclass) NOT NULL,
    name_type_task_area character varying(100)
);


ALTER TABLE type_task_area OWNER TO evgenia;

--
-- TOC entry 175 (class 1259 OID 139278)
-- Name: user_id_user_seq; Type: SEQUENCE; Schema: public; Owner: evgenia
--

CREATE SEQUENCE user_id_user_seq
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_user_seq OWNER TO evgenia;

--
-- TOC entry 177 (class 1259 OID 139289)
-- Name: users; Type: TABLE; Schema: public; Owner: evgenia
--

CREATE TABLE users (
    id_user integer DEFAULT nextval('user_id_user_seq'::regclass) NOT NULL,
    id_access_level integer,
    login character varying,
    password character varying,
    name_user character varying,
    status_account integer
);


ALTER TABLE users OWNER TO evgenia;

--
-- TOC entry 2247 (class 0 OID 0)
-- Dependencies: 174
-- Name: access_level_id_access_level_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('access_level_id_access_level_seq', 4, true);


--
-- TOC entry 2212 (class 0 OID 139280)
-- Dependencies: 176
-- Data for Name: access_levels; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY access_levels (id_access_level, name_access_level) FROM stdin;
2	Администратор
3	Эксперт
4	Специалист
\.


--
-- TOC entry 2218 (class 0 OID 147469)
-- Dependencies: 182
-- Data for Name: algorithm_class; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY algorithm_class (id_algorithm_class, name_algorithm_class) FROM stdin;
1	Детермирированный
2	Вероятностный
\.


--
-- TOC entry 2248 (class 0 OID 0)
-- Dependencies: 180
-- Name: algorithm_class_id_algorithm_class_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('algorithm_class_id_algorithm_class_seq', 2, true);


--
-- TOC entry 2222 (class 0 OID 147504)
-- Dependencies: 186
-- Data for Name: application_area; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY application_area (id_application_area, name_application_area) FROM stdin;
1	Криптография
2	Цифровая обработка сигналов
\.


--
-- TOC entry 2249 (class 0 OID 0)
-- Dependencies: 185
-- Name: application_area_id_application_area_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('application_area_id_application_area_seq', 2, true);


--
-- TOC entry 2217 (class 0 OID 147463)
-- Dependencies: 181
-- Data for Name: complexity_class; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY complexity_class (id_complexity_class, name_complexity_class) FROM stdin;
1	Экспоненциальный
2	Субэкспоненциальный
3	Полиномиальный
\.


--
-- TOC entry 2250 (class 0 OID 0)
-- Dependencies: 179
-- Name: complexity_class_id_complexity_class_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('complexity_class_id_complexity_class_seq', 3, true);


--
-- TOC entry 2238 (class 0 OID 163858)
-- Dependencies: 202
-- Data for Name: logbook_update; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY logbook_update (id_logbook_update, id_method, id_user, status_change, date_change) FROM stdin;
2	2	2	Добавление	2021-12-27
4	4	2	Добавление	2022-02-21
9	\N	2	Изменение	2022-03-02
10	\N	2	Изменение	2022-03-02
11	4	2	Изменение	2022-03-02
12	4	2	Изменение	2022-03-02
13	2	2	Изменение	2022-03-02
3	3	2	Добавление	2022-01-09
8	8	2	Добавление	2022-02-01
16	11	2	Добавление	2022-02-17
17	12	2	Добавление	2022-03-04
18	13	2	Добавление	2022-02-14
19	14	2	Добавление	2022-03-26
20	\N	2	Изменение	2022-06-02
21	\N	2	Изменение	2022-06-02
\.


--
-- TOC entry 2251 (class 0 OID 0)
-- Dependencies: 201
-- Name: logbook_update_id_logbook_update_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('logbook_update_id_logbook_update_seq', 21, true);


--
-- TOC entry 2228 (class 0 OID 147543)
-- Dependencies: 192
-- Data for Name: method; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY method (id_method, name_method, numb_stages, value_memory, description_stages, simplified_code, complexity_method, id_algorithm_class, id_complexity_class, status_method) FROM stdin;
3	Тест Соловея-Штрассена	5		1. Р’ С†РёРєР»Рµ i РѕС‚ 1 РґРѕ k РІС‹РїРѕР»РЅРёС‚СЊ:\n 1.1. Р’С‹Р±СЂР°С‚СЊ a - СЃР»СѓС‡Р°Р№РЅРѕРµ С†РµР»РѕРµ РѕС‚ 2 РґРѕ n-1 РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ;\n 1.2. Р•СЃР»Рё РќРћР”(a,n) > 1, С‚РѕРіРґР° РІРµСЂРЅСѓС‚СЊ - СЃРѕСЃС‚Р°РІРЅРѕРµ;\n 1.3. Р•СЃР»Рё a^((n-1)/2) РЅРµ СЂР°РІРЅРѕ (a/n)(mod n), С‚РѕРіРґР° РІРµСЂРЅСѓС‚СЊ - СЃРѕСЃС‚Р°РІРЅРѕРµ;\n2. Р’РµСЂРЅСѓС‚СЊ - РїСЂРѕСЃС‚РѕРµ СЃ РІРµСЂРѕСЏС‚РЅРѕСЃС‚СЊСЋ 1-2^(-k)		O(log^3 n)	2	3	0
8	Тест Миллера-Рабина	11	-			O(log^3 n)	2	3	0
4	тест Люка-Лемера	5				O(s^3)	1	3	0
2	Тест Ферма	5		1. В цикл i до t выполнить:\n  1.1. Выбрать случейное 2<=a<=n-2.\n  1.2. Вычислить r = a^(n-1) (mod n).\n  1.3. Если r не равно 1, тогда вернуть: n - составное.\n2. Вернуть: n - простое.		O(log^3 n)	2	3	0
11	Ро-метод Полларда	5				O(n^(1/4))	2	1	0
12	Алгоритм факторизации Ленстры	11				L_p (1/2, sqrt(2))	1	2	0
13	Базовый метод QS	12				L_p(1/2, 1)	1	2	0
14	Базовый метод NFS	25				L_p(1/3, (64/9)^(1/3))	1	2	0
\.


--
-- TOC entry 2236 (class 0 OID 147606)
-- Dependencies: 200
-- Data for Name: method_constraint; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY method_constraint (id_method_constraint, id_method, id_possib_constraint) FROM stdin;
1	2	1
2	8	3
\.


--
-- TOC entry 2252 (class 0 OID 0)
-- Dependencies: 199
-- Name: method_constraint_id_method_constraint; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('method_constraint_id_method_constraint', 4, true);


--
-- TOC entry 2253 (class 0 OID 0)
-- Dependencies: 191
-- Name: method_id_method_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('method_id_method_seq', 14, true);


--
-- TOC entry 2232 (class 0 OID 147579)
-- Dependencies: 196
-- Data for Name: method_task_area; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY method_task_area (id_method_task_area, id_method, id_task_area) FROM stdin;
1	2	3
2	3	3
4	4	3
9	8	3
12	3	4
14	11	5
15	12	5
16	13	5
17	14	5
\.


--
-- TOC entry 2254 (class 0 OID 0)
-- Dependencies: 195
-- Name: method_task_area_id_method_task_area; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('method_task_area_id_method_task_area', 17, true);


--
-- TOC entry 2230 (class 0 OID 147559)
-- Dependencies: 194
-- Data for Name: method_theorem; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY method_theorem (id_method_theorem, id_method, id_theorem) FROM stdin;
1	2	1
2	8	3
6	11	5
\.


--
-- TOC entry 2255 (class 0 OID 0)
-- Dependencies: 193
-- Name: method_theorem_id_method_theorem; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('method_theorem_id_method_theorem', 7, true);


--
-- TOC entry 2234 (class 0 OID 147598)
-- Dependencies: 198
-- Data for Name: possib_constraint; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY possib_constraint (id_possib_constraint, name_possib_constraint) FROM stdin;
1	Числа Кармайкла
2	Работает для чисел Мерсенна
3	Результат с вероятностью 4^(-r)
\.


--
-- TOC entry 2256 (class 0 OID 0)
-- Dependencies: 197
-- Name: possib_constraint_id_possib_constraint; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('possib_constraint_id_possib_constraint', 3, true);


--
-- TOC entry 2226 (class 0 OID 147525)
-- Dependencies: 190
-- Data for Name: pract_task_area; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY pract_task_area (id_pract_task_area, id_task_area, id_practical_task) FROM stdin;
1	4	1
2	2	2
3	3	2
4	2	1
5	3	1
\.


--
-- TOC entry 2257 (class 0 OID 0)
-- Dependencies: 189
-- Name: pract_task_area_id_pract_task_area_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('pract_task_area_id_pract_task_area_seq', 6, true);


--
-- TOC entry 2224 (class 0 OID 147512)
-- Dependencies: 188
-- Data for Name: practical_task; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY practical_task (id_practical_task, id_application_area, name_practical_task) FROM stdin;
1	1	Алгоритм RSA
2	1	Цифровая подпись
3	2	Алгоритм Гёрцеля
\.


--
-- TOC entry 2258 (class 0 OID 0)
-- Dependencies: 187
-- Name: practical_task_id_practical_task_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('practical_task_id_practical_task_seq', 3, true);


--
-- TOC entry 2214 (class 0 OID 139300)
-- Dependencies: 178
-- Data for Name: task_area; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY task_area (id_task_area, id_type_task_area, name_task_area) FROM stdin;
2	1	Тестирование на простоту чисел произвольного вида
3	1	Тестирование на простоту чисел специального вида
4	1	Поиск псевдопростых чисел
5	1	Факторизация
\.


--
-- TOC entry 2259 (class 0 OID 0)
-- Dependencies: 173
-- Name: task_area_id_task_area_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('task_area_id_task_area_seq', 5, true);


--
-- TOC entry 2220 (class 0 OID 147493)
-- Dependencies: 184
-- Data for Name: theorem; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY theorem (id_theorem, name_theorem, statement_theorem, name_resource) FROM stdin;
1	Малая теорема Ферма	Если n - простое число и a - любое целое число, 1<=a<=n-1, тогда a^(n-1) эквивалентно 1(mod n).	
2	Критерий Эйлера	РќРµС‡РµС‚РЅРѕРµ С‡РёСЃР»Рѕ n СЏРІР»СЏРµС‚СЃСЏ РїСЂРѕСЃС‚С‹Рј С‚РѕРіРґР° Рё С‚РѕР»СЊРєРѕ С‚РѕРіРґР°, \nРєРѕРіРґР° РґР»СЏ Р»СЋР±РѕРіРѕ С†РµР»РѕРіРѕ С‡РёСЃР»Р° a, 1 <= a <= n-1, \nРІР·Р°РёРјРЅРѕ РїСЂРѕСЃС‚РѕРіРѕ СЃ n, РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ СЃСЂР°РІРЅРµРЅРёРµ:\na^((n-1)/2) СЌРєРІРёРІР°Р»РµРЅС‚РЅРѕ (a/n)(mod n),\nРіРґРµ (a/n) - СЃРёРјРІРѕР» РЇРєРѕР±Рё РѕС‚ РїР°СЂР°РјРµС‚СЂРѕРІ a Рё n.	
5	Парадокс дня рождения	РџСѓСЃС‚СЊ lamb > 0. Р”Р»СЏ СЃР»СѓС‡Р°Р№РЅРѕР№ РІС‹Р±РѕСЂРєРё l + l СЌР»РµРјРµРЅС‚РѕРІ,\nРєР°Р¶РґС‹Р№ РёР· РєРѕС‚РѕСЂС‹С… РјРµРЅСЊС€Рµ q, РіРґРµ l = sqrt(2 * lamb * q),\nРІРµСЂРѕСЏС‚РЅРѕСЃС‚СЊ С‚РѕРіРѕ, С‡С‚Рѕ РґРІР° СЌР»РµРјРµРЅС‚Р° РѕРєР°Р¶СѓС‚СЃСЏ СЂР°РІРЅС‹РјРё \np > 1 - e^(-lamb)	
3	Теорема Рабина	РЎРѕСЃС‚Р°РІРЅРѕРµ РЅРµС‡РµС‚РЅРѕРµ n РёРјРµРµС‚ РЅРµ Р±РѕР»РµРµ fi(n)/4 СЂР°Р·Р»РёС‡РЅС‹С…\nСЃРІРёРґРµС‚РµР»РµР№ РїСЂРѕСЃС‚РѕС‚С‹, РіРґРµ fi(n) - С„СѓРЅРєС†РёСЏ Р­Р№Р»РµСЂР°.	
6	Китайская теорема об остатках	Р•СЃР»Рё РЅР°С‚СѓСЂР°Р»СЊРЅС‹Рµ С‡РёСЃР»Р° a_1, a_2, ..., a_n РїРѕРїР°СЂРЅРѕ РІР·Р°РёРјРЅРѕ\nРїСЂРѕСЃС‚С‹, С‚Рѕ РґР»СЏ Р»СЋР±С‹С… С†РµР»С‹С… r_1, r_2, ..., r_n С‚Р°РєРёС…, С‡С‚Рѕ\n0 <= r_i <= a_i РїСЂРё РІСЃРµС… i РїСЂРёРЅР°РґР»РµР¶Р°С‰РёС… {1, 2, ..., n}.\nР‘РѕР»РµРµ С‚РѕРіРѕ, РµСЃР»Рё РЅР°Р№РґСѓС‚СЃСЏ РґРІР° С‚Р°РєРёС… С‡РёСЃР»Р° N_1 Рё N_2 \n(СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёС… СѓС‚РІРµСЂР¶РґРµРЅРёСЋ РІС‹С€Рµ), С‚Рѕ \nN_1 СЌРєРІРёРІР°Р»РµРЅС‚РЅРѕ N_2 (mod a_1 * a_2 * ... * a_n).	
\.


--
-- TOC entry 2260 (class 0 OID 0)
-- Dependencies: 183
-- Name: theorem_id_theorem_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('theorem_id_theorem_seq', 6, true);


--
-- TOC entry 2208 (class 0 OID 139268)
-- Dependencies: 172
-- Data for Name: type_task_area; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY type_task_area (id_type_task_area, name_type_task_area) FROM stdin;
1	Теория чисел
\.


--
-- TOC entry 2261 (class 0 OID 0)
-- Dependencies: 171
-- Name: type_task_area_id_type_task_area_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('type_task_area_id_type_task_area_seq', 1, true);


--
-- TOC entry 2262 (class 0 OID 0)
-- Dependencies: 175
-- Name: user_id_user_seq; Type: SEQUENCE SET; Schema: public; Owner: evgenia
--

SELECT pg_catalog.setval('user_id_user_seq', 4, true);


--
-- TOC entry 2213 (class 0 OID 139289)
-- Dependencies: 177
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: evgenia
--

COPY users (id_user, id_access_level, login, password, name_user, status_account) FROM stdin;
2	2	admin	a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057	Сапунова Евгения Сергеевна	0
3	3	newuser	a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057	Степанов Степан Степанович	0
4	4	simpuser	a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057	Петров Петр Петрович	0
\.


--
-- TOC entry 2056 (class 2606 OID 139288)
-- Name: access_level_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY access_levels
    ADD CONSTRAINT access_level_pkey PRIMARY KEY (id_access_level);


--
-- TOC entry 2064 (class 2606 OID 147474)
-- Name: algorithm_class_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY algorithm_class
    ADD CONSTRAINT algorithm_class_pkey PRIMARY KEY (id_algorithm_class);


--
-- TOC entry 2068 (class 2606 OID 147509)
-- Name: application_area_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY application_area
    ADD CONSTRAINT application_area_pkey PRIMARY KEY (id_application_area);


--
-- TOC entry 2062 (class 2606 OID 147468)
-- Name: complexity_class_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY complexity_class
    ADD CONSTRAINT complexity_class_pkey PRIMARY KEY (id_complexity_class);


--
-- TOC entry 2084 (class 2606 OID 163863)
-- Name: logbook_update_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY logbook_update
    ADD CONSTRAINT logbook_update_pkey PRIMARY KEY (id_logbook_update);


--
-- TOC entry 2082 (class 2606 OID 147611)
-- Name: method_constraint_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_constraint
    ADD CONSTRAINT method_constraint_pkey PRIMARY KEY (id_method_constraint);


--
-- TOC entry 2074 (class 2606 OID 147551)
-- Name: method_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method
    ADD CONSTRAINT method_pkey PRIMARY KEY (id_method);


--
-- TOC entry 2078 (class 2606 OID 147584)
-- Name: method_task_area_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_task_area
    ADD CONSTRAINT method_task_area_pkey PRIMARY KEY (id_method_task_area);


--
-- TOC entry 2076 (class 2606 OID 147564)
-- Name: method_theorem_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_theorem
    ADD CONSTRAINT method_theorem_pkey PRIMARY KEY (id_method_theorem);


--
-- TOC entry 2080 (class 2606 OID 147603)
-- Name: possib_constraint_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY possib_constraint
    ADD CONSTRAINT possib_constraint_pkey PRIMARY KEY (id_possib_constraint);


--
-- TOC entry 2072 (class 2606 OID 147530)
-- Name: pract_task_area_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY pract_task_area
    ADD CONSTRAINT pract_task_area_pkey PRIMARY KEY (id_pract_task_area);


--
-- TOC entry 2070 (class 2606 OID 147517)
-- Name: practical_task_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY practical_task
    ADD CONSTRAINT practical_task_pkey PRIMARY KEY (id_practical_task);


--
-- TOC entry 2060 (class 2606 OID 139305)
-- Name: task_area_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY task_area
    ADD CONSTRAINT task_area_pkey PRIMARY KEY (id_task_area);


--
-- TOC entry 2066 (class 2606 OID 147501)
-- Name: theorem_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY theorem
    ADD CONSTRAINT theorem_pkey PRIMARY KEY (id_theorem);


--
-- TOC entry 2054 (class 2606 OID 139273)
-- Name: type_task_area_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY type_task_area
    ADD CONSTRAINT type_task_area_pkey PRIMARY KEY (id_type_task_area);


--
-- TOC entry 2058 (class 2606 OID 139294)
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY users
    ADD CONSTRAINT user_pkey PRIMARY KEY (id_user);


--
-- TOC entry 2091 (class 2606 OID 163851)
-- Name: algorithm_class_id_algorithm_class_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method
    ADD CONSTRAINT algorithm_class_id_algorithm_class_fkey FOREIGN KEY (id_algorithm_class) REFERENCES algorithm_class(id_algorithm_class);


--
-- TOC entry 2087 (class 2606 OID 147518)
-- Name: application_area_id_application_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY practical_task
    ADD CONSTRAINT application_area_id_application_area_fkey FOREIGN KEY (id_application_area) REFERENCES application_area(id_application_area);


--
-- TOC entry 2090 (class 2606 OID 163846)
-- Name: complexity_class_id_complexity_class_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method
    ADD CONSTRAINT complexity_class_id_complexity_class_fkey FOREIGN KEY (id_complexity_class) REFERENCES complexity_class(id_complexity_class);


--
-- TOC entry 2092 (class 2606 OID 147565)
-- Name: method_id_method_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_theorem
    ADD CONSTRAINT method_id_method_fkey FOREIGN KEY (id_method) REFERENCES method(id_method);


--
-- TOC entry 2094 (class 2606 OID 147585)
-- Name: method_id_method_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_task_area
    ADD CONSTRAINT method_id_method_fkey FOREIGN KEY (id_method) REFERENCES method(id_method);


--
-- TOC entry 2096 (class 2606 OID 147612)
-- Name: method_id_method_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_constraint
    ADD CONSTRAINT method_id_method_fkey FOREIGN KEY (id_method) REFERENCES method(id_method);


--
-- TOC entry 2098 (class 2606 OID 163864)
-- Name: method_id_method_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY logbook_update
    ADD CONSTRAINT method_id_method_fkey FOREIGN KEY (id_method) REFERENCES method(id_method);


--
-- TOC entry 2097 (class 2606 OID 147617)
-- Name: possib_constraint_id_possib_constraint_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_constraint
    ADD CONSTRAINT possib_constraint_id_possib_constraint_fkey FOREIGN KEY (id_possib_constraint) REFERENCES possib_constraint(id_possib_constraint);


--
-- TOC entry 2089 (class 2606 OID 147536)
-- Name: practical_task_id_practical_task_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY pract_task_area
    ADD CONSTRAINT practical_task_id_practical_task_fkey FOREIGN KEY (id_practical_task) REFERENCES practical_task(id_practical_task);


--
-- TOC entry 2088 (class 2606 OID 147531)
-- Name: task_area_id_task_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY pract_task_area
    ADD CONSTRAINT task_area_id_task_area_fkey FOREIGN KEY (id_task_area) REFERENCES task_area(id_task_area);


--
-- TOC entry 2095 (class 2606 OID 147590)
-- Name: task_area_id_task_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_task_area
    ADD CONSTRAINT task_area_id_task_area_fkey FOREIGN KEY (id_task_area) REFERENCES task_area(id_task_area);


--
-- TOC entry 2086 (class 2606 OID 139306)
-- Name: task_area_id_type_task_area_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY task_area
    ADD CONSTRAINT task_area_id_type_task_area_fkey FOREIGN KEY (id_type_task_area) REFERENCES type_task_area(id_type_task_area);


--
-- TOC entry 2093 (class 2606 OID 147570)
-- Name: theorem_id_theorem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY method_theorem
    ADD CONSTRAINT theorem_id_theorem_fkey FOREIGN KEY (id_theorem) REFERENCES theorem(id_theorem);


--
-- TOC entry 2085 (class 2606 OID 139295)
-- Name: users_id_access_level_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_id_access_level_fkey FOREIGN KEY (id_access_level) REFERENCES access_levels(id_access_level);


--
-- TOC entry 2099 (class 2606 OID 163869)
-- Name: users_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evgenia
--

ALTER TABLE ONLY logbook_update
    ADD CONSTRAINT users_id_user_fkey FOREIGN KEY (id_user) REFERENCES users(id_user);


--
-- TOC entry 2245 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2022-06-02 06:14:28

--
-- PostgreSQL database dump complete
--

