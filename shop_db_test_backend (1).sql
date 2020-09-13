PGDMP                         x           shop_db2    12.2    12.2                 0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            !           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            "           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            #           1262    16751    shop_db2    DATABASE     �   CREATE DATABASE shop_db2 WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Polish_Poland.1250' LC_CTYPE = 'Polish_Poland.1250';
    DROP DATABASE shop_db2;
                postgres    false                        3079    16752 	   adminpack 	   EXTENSION     A   CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;
    DROP EXTENSION adminpack;
                   false            $           0    0    EXTENSION adminpack    COMMENT     M   COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';
                        false    1            �            1259    16761 	   available    TABLE     �   CREATE TABLE public.available (
    batch_id integer NOT NULL,
    product_barcode text NOT NULL,
    expiration_date date NOT NULL,
    quantity integer NOT NULL,
    weight real NOT NULL
);
    DROP TABLE public.available;
       public         heap    postgres    false            �            1259    16767    products    TABLE     �   CREATE TABLE public.products (
    barcode text NOT NULL,
    name text NOT NULL,
    category text NOT NULL,
    price money NOT NULL
);
    DROP TABLE public.products;
       public         heap    postgres    false            �            1259    16773    sold    TABLE     �   CREATE TABLE public.sold (
    product_barcode text NOT NULL,
    expiration_date date NOT NULL,
    quantity integer NOT NULL,
    weight real NOT NULL,
    batch_id integer NOT NULL
);
    DROP TABLE public.sold;
       public         heap    postgres    false            �            1259    16793    sold_batch_id_seq    SEQUENCE     �   ALTER TABLE public.sold ALTER COLUMN batch_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.sold_batch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    205            �            1259    16779    wasted    TABLE     �   CREATE TABLE public.wasted (
    batch_id integer NOT NULL,
    product_barcode text NOT NULL,
    expiration_date date NOT NULL,
    quantity integer NOT NULL,
    weight real NOT NULL
);
    DROP TABLE public.wasted;
       public         heap    postgres    false            �            1259    16795    wasted_batch_id_seq    SEQUENCE     �   ALTER TABLE public.wasted ALTER COLUMN batch_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.wasted_batch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    206                      0    16761 	   available 
   TABLE DATA           a   COPY public.available (batch_id, product_barcode, expiration_date, quantity, weight) FROM stdin;
    public          postgres    false    203   �                 0    16767    products 
   TABLE DATA           B   COPY public.products (barcode, name, category, price) FROM stdin;
    public          postgres    false    204   >                 0    16773    sold 
   TABLE DATA           \   COPY public.sold (product_barcode, expiration_date, quantity, weight, batch_id) FROM stdin;
    public          postgres    false    205   �                 0    16779    wasted 
   TABLE DATA           ^   COPY public.wasted (batch_id, product_barcode, expiration_date, quantity, weight) FROM stdin;
    public          postgres    false    206   �       %           0    0    sold_batch_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.sold_batch_id_seq', 10804, true);
          public          postgres    false    207            &           0    0    wasted_batch_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.wasted_batch_id_seq', 3, true);
          public          postgres    false    208            �
           2606    16786    available avaliable_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.available
    ADD CONSTRAINT avaliable_pkey PRIMARY KEY (batch_id);
 B   ALTER TABLE ONLY public.available DROP CONSTRAINT avaliable_pkey;
       public            postgres    false    203            �
           2606    16788    products product_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.products
    ADD CONSTRAINT product_pkey PRIMARY KEY (barcode);
 ?   ALTER TABLE ONLY public.products DROP CONSTRAINT product_pkey;
       public            postgres    false    204            �
           2606    16790    sold sold_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.sold
    ADD CONSTRAINT sold_pkey PRIMARY KEY (batch_id);
 8   ALTER TABLE ONLY public.sold DROP CONSTRAINT sold_pkey;
       public            postgres    false    205            �
           2606    16792    wasted wasted_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.wasted
    ADD CONSTRAINT wasted_pkey PRIMARY KEY (batch_id);
 <   ALTER TABLE ONLY public.wasted DROP CONSTRAINT wasted_pkey;
       public            postgres    false    206               C   x�U���0���K*0I���sT)�gG@&�ȡ���:RQ 8�����S��z�=$76e�         ?   x�3�t.M.�MJ-�,KMO-IL�I-�4�15P�:��e�_ژ�9#3��855I��h� �?"Y         <   x�3�4202�5"CNCNSNCsKK.cda� P��� ��!va#��ƨPa�=... j��         #   x�3�4�4202�5"CN �2�2������ '�	+     