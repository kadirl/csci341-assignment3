--
-- PostgreSQL database dump
--

\restrict T3Rz1NfCpDM5KWyfPErfuHur28xVy5fMChtK7sBRqFEb6MhBPM9RuucIwmbcFtp

-- Dumped from database version 16.11 (Homebrew)
-- Dumped by pg_dump version 16.11 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: address; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public.address (
    member_user_id integer NOT NULL,
    house_number character varying(20) NOT NULL,
    street character varying(255) NOT NULL,
    town character varying(100) NOT NULL
);


ALTER TABLE public.address OWNER TO macbookair;

--
-- Name: appointment; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public.appointment (
    appointment_id integer NOT NULL,
    caregiver_user_id integer NOT NULL,
    member_user_id integer NOT NULL,
    appointment_date date NOT NULL,
    appointment_time time without time zone NOT NULL,
    work_hours numeric(5,2) NOT NULL,
    status character varying(20) NOT NULL,
    CONSTRAINT check_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'accepted'::character varying, 'declined'::character varying])::text[])))
);


ALTER TABLE public.appointment OWNER TO macbookair;

--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE; Schema: public; Owner: macbookair
--

CREATE SEQUENCE public.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.appointment_appointment_id_seq OWNER TO macbookair;

--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: macbookair
--

ALTER SEQUENCE public.appointment_appointment_id_seq OWNED BY public.appointment.appointment_id;


--
-- Name: caregiver; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public.caregiver (
    caregiver_user_id integer NOT NULL,
    photo character varying(255),
    gender character varying(20) NOT NULL,
    caregiving_type character varying(50) NOT NULL,
    hourly_rate numeric(10,2) NOT NULL,
    CONSTRAINT check_caregiving_type CHECK (((caregiving_type)::text = ANY ((ARRAY['babysitter'::character varying, 'elderly care'::character varying, 'playmate for children'::character varying])::text[])))
);


ALTER TABLE public.caregiver OWNER TO macbookair;

--
-- Name: job; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public.job (
    job_id integer NOT NULL,
    member_user_id integer NOT NULL,
    required_caregiving_type character varying(50) NOT NULL,
    other_requirements text,
    date_posted date NOT NULL,
    CONSTRAINT check_required_caregiving_type CHECK (((required_caregiving_type)::text = ANY ((ARRAY['babysitter'::character varying, 'elderly care'::character varying, 'playmate for children'::character varying])::text[])))
);


ALTER TABLE public.job OWNER TO macbookair;

--
-- Name: job_application; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public.job_application (
    caregiver_user_id integer NOT NULL,
    job_id integer NOT NULL,
    date_applied date NOT NULL
);


ALTER TABLE public.job_application OWNER TO macbookair;

--
-- Name: user; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public."user" (
    user_id integer NOT NULL,
    email character varying(255) NOT NULL,
    given_name character varying(100) NOT NULL,
    surname character varying(100) NOT NULL,
    city character varying(100) NOT NULL,
    phone_number character varying(20) NOT NULL,
    profile_description text,
    password character varying(255) NOT NULL
);


ALTER TABLE public."user" OWNER TO macbookair;

--
-- Name: job_applications_view; Type: VIEW; Schema: public; Owner: macbookair
--

CREATE VIEW public.job_applications_view AS
 SELECT ja.job_id,
    j.required_caregiving_type,
    j.other_requirements,
    j.date_posted,
    ja.caregiver_user_id,
    (((u.given_name)::text || ' '::text) || (u.surname)::text) AS applicant_name,
    c.caregiving_type,
    c.hourly_rate,
    ja.date_applied
   FROM (((public.job_application ja
     JOIN public.job j ON ((ja.job_id = j.job_id)))
     JOIN public.caregiver c ON ((ja.caregiver_user_id = c.caregiver_user_id)))
     JOIN public."user" u ON ((c.caregiver_user_id = u.user_id)));


ALTER VIEW public.job_applications_view OWNER TO macbookair;

--
-- Name: job_job_id_seq; Type: SEQUENCE; Schema: public; Owner: macbookair
--

CREATE SEQUENCE public.job_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_job_id_seq OWNER TO macbookair;

--
-- Name: job_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: macbookair
--

ALTER SEQUENCE public.job_job_id_seq OWNED BY public.job.job_id;


--
-- Name: member; Type: TABLE; Schema: public; Owner: macbookair
--

CREATE TABLE public.member (
    member_user_id integer NOT NULL,
    house_rules text,
    dependent_description text
);


ALTER TABLE public.member OWNER TO macbookair;

--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: macbookair
--

CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_user_id_seq OWNER TO macbookair;

--
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: macbookair
--

ALTER SEQUENCE public.user_user_id_seq OWNED BY public."user".user_id;


--
-- Name: appointment appointment_id; Type: DEFAULT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('public.appointment_appointment_id_seq'::regclass);


--
-- Name: job job_id; Type: DEFAULT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.job ALTER COLUMN job_id SET DEFAULT nextval('public.job_job_id_seq'::regclass);


--
-- Name: user user_id; Type: DEFAULT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public."user" ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);


--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public.address (member_user_id, house_number, street, town) FROM stdin;
4	22	Abay Avenue	Astana
9	44	Al-Farabi Avenue	Almaty
13	66	Tauelsizdik Avenue	Shymkent
16	88	Abay Avenue	Astana
18	99	Al-Farabi Avenue	Almaty
\.


--
-- Data for Name: appointment; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public.appointment (appointment_id, caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) FROM stdin;
3	5	4	2025-02-12	10:00:00	5.00	accepted
4	8	9	2025-02-13	15:00:00	3.50	accepted
5	10	13	2025-02-14	08:00:00	6.00	accepted
7	17	18	2025-02-16	11:00:00	4.00	accepted
10	5	16	2025-02-19	10:00:00	4.00	accepted
12	10	4	2025-02-21	11:00:00	4.00	pending
13	3	9	2025-02-22	15:00:00	2.00	declined
15	14	18	2025-02-24	12:00:00	4.00	declined
\.


--
-- Data for Name: caregiver; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public.caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) FROM stdin;
1	photo1.jpg	Male	babysitter	8.80
3	photo3.jpg	Male	babysitter	9.30
5	photo5.jpg	Male	elderly care	13.20
7	photo7.jpg	Male	playmate for children	7.80
8	photo8.jpg	Female	babysitter	11.00
10	photo10.jpg	Female	elderly care	12.65
12	photo12.jpg	Male	babysitter	9.80
14	photo14.jpg	Male	playmate for children	8.30
17	photo17.jpg	Female	babysitter	11.55
19	photo19.jpg	Female	elderly care	14.30
20	photo20.jpg	Male	playmate for children	7.30
\.


--
-- Data for Name: job; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public.job (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted) FROM stdin;
2	4	elderly care	Experience with dementia patients preferred	2025-01-16
4	9	babysitter	Energetic and fun-loving	2025-01-18
6	13	elderly care	Medical training preferred	2025-01-20
8	16	elderly care	Soft-spoken caregiver needed	2025-01-22
9	18	playmate for children	Active and engaging	2025-01-23
11	4	elderly care	Morning shifts preferred	2025-01-25
13	9	playmate for children	Outdoor activities preferred	2025-01-27
15	13	elderly care	Evening care needed	2025-01-29
\.


--
-- Data for Name: job_application; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public.job_application (caregiver_user_id, job_id, date_applied) FROM stdin;
1	2	2025-01-25
5	2	2025-01-26
10	2	2025-01-27
19	2	2025-01-28
5	6	2025-02-06
10	6	2025-02-07
19	6	2025-02-08
5	8	2025-02-12
10	8	2025-02-13
19	8	2025-02-14
7	9	2025-02-15
14	9	2025-02-16
20	9	2025-02-17
8	4	2025-11-21
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public.member (member_user_id, house_rules, dependent_description) FROM stdin;
4	No pets. Quiet environment required.	Elderly mother needs daily care, age 75
9	Pets allowed. Respectful behavior.	Two children aged 4 and 6 need babysitting
13	No pets. Professional care required.	Elderly father, age 80, needs assistance
16	No pets. Soft-spoken caregiver preferred.	Elderly parent needs gentle care
18	Pets allowed. Flexible schedule.	Three children need playmate and supervision
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: macbookair
--

COPY public."user" (user_id, email, given_name, surname, city, phone_number, profile_description, password) FROM stdin;
2	amina.aminova@email.com	Amina	Aminova	Almaty	+77772345678	Family member seeking care	password123
3	david.davidov@email.com	David	Davidov	Astana	+77773456789	Professional babysitter	password123
4	elena.elenova@email.com	Elena	Elenova	Astana	+77774567890	Looking for elderly care	password123
5	farid.faridov@email.com	Farid	Faridov	Almaty	+77775678901	Elderly care specialist	password123
6	gulnara.gulnarova@email.com	Gulnara	Gulnarova	Astana	+77776789012	Mother of two children	password123
7	hasan.hasanov@email.com	Hasan	Hasanov	Shymkent	+77777890123	Playmate for children	password123
8	irina.irinova@email.com	Irina	Irinova	Astana	+77778901234	Babysitter with 5 years experience	password123
9	john.johnson@email.com	John	Johnson	Almaty	+77779012345	Father seeking babysitter	password123
10	kate.kateova@email.com	Kate	Kateova	Astana	+77770123456	Elderly care professional	password123
11	lisa.lisova@email.com	Lisa	Lisova	Astana	+77771234560	Mother of 5-year-old son	password123
12	michael.michaelov@email.com	Michael	Michaelov	Almaty	+77772345601	Babysitter	password123
13	nina.ninova@email.com	Nina	Ninova	Shymkent	+77773456712	Family member	password123
14	omar.omarov@email.com	Omar	Omarov	Astana	+77774567823	Playmate specialist	password123
15	paul.paulov@email.com	Paul	Paulov	Astana	+77775678934	Seeking elderly care	password123
16	qasim.qasimov@email.com	Qasim	Qasimov	Almaty	+77776789045	Elderly care expert	password123
17	rosa.rosova@email.com	Rosa	Rosova	Astana	+77777890156	Babysitter	password123
18	sam.samov@email.com	Sam	Samov	Shymkent	+77778901267	Father of three	password123
19	tina.tinova@email.com	Tina	Tinova	Astana	+77779012378	Elderly care professional	password123
20	umar.umarov@email.com	Umar	Umarov	Almaty	+77770123489	Playmate for children	password123
1	arman.armanov@email.com	Arman	Armanov	Astana	+77773414141	Experienced caregiver	password123
\.


--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: macbookair
--

SELECT pg_catalog.setval('public.appointment_appointment_id_seq', 15, true);


--
-- Name: job_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: macbookair
--

SELECT pg_catalog.setval('public.job_job_id_seq', 15, true);


--
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: macbookair
--

SELECT pg_catalog.setval('public.user_user_id_seq', 22, true);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (member_user_id);


--
-- Name: appointment appointment_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);


--
-- Name: caregiver caregiver_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.caregiver
    ADD CONSTRAINT caregiver_pkey PRIMARY KEY (caregiver_user_id);


--
-- Name: job_application job_application_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.job_application
    ADD CONSTRAINT job_application_pkey PRIMARY KEY (caregiver_user_id, job_id);


--
-- Name: job job_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_pkey PRIMARY KEY (job_id);


--
-- Name: member member_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_pkey PRIMARY KEY (member_user_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: address address_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public.member(member_user_id) ON DELETE CASCADE;


--
-- Name: appointment appointment_caregiver_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_caregiver_user_id_fkey FOREIGN KEY (caregiver_user_id) REFERENCES public.caregiver(caregiver_user_id) ON DELETE CASCADE;


--
-- Name: appointment appointment_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public.member(member_user_id) ON DELETE CASCADE;


--
-- Name: caregiver caregiver_caregiver_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.caregiver
    ADD CONSTRAINT caregiver_caregiver_user_id_fkey FOREIGN KEY (caregiver_user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- Name: job_application job_application_caregiver_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.job_application
    ADD CONSTRAINT job_application_caregiver_user_id_fkey FOREIGN KEY (caregiver_user_id) REFERENCES public.caregiver(caregiver_user_id) ON DELETE CASCADE;


--
-- Name: job_application job_application_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.job_application
    ADD CONSTRAINT job_application_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job(job_id) ON DELETE CASCADE;


--
-- Name: job job_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public.member(member_user_id) ON DELETE CASCADE;


--
-- Name: member member_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: macbookair
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict T3Rz1NfCpDM5KWyfPErfuHur28xVy5fMChtK7sBRqFEb6MhBPM9RuucIwmbcFtp

