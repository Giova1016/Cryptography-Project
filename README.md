# Cryptography Algorithms

This project is a working prototype for many Cryptography algorithms made in Python.

## Table of Contents
- [Introduction](#introduction)
- [About](#about)
- [How to Download](#how_to_download)

## Introduction

This is a project made for an Introduction to Cryptography course.
The project aimed for students to program the cryptographic algorithms discussed during the course to solidify and apply what we learned.

## About

The code from this project can be downloaded and executed by anyone with an appropriate Python interpreter and there are many algorithms to choose from, including:
- Affine Cipher
- Stream Cipher
- Generation of keys using a Linear Feedback Shift Register (LFSR)
- Data Encryption Standard (DES)
- Advanced Encryption Standard (AES)
- RSA with key generation
- Square-and_multiply for modular exponentiation
- Fermat and Miller-Rabin Primality Test
- ElGamal protocol based on the Diffie-Hellman Key Exchange (DHKE)
- DHKE based on Elliptic Curves

## How to Download

To download the programs in this repository you can follow this guide:
- First of all, It is required for you to have a working Python interpreter as stated before, you can download one from an official website or the Microsoft store.
- Another option is to have an IDE that has Python or that you can install a Python extension like Visual Studio Code.
- Once that is done, I recommend you change the directory to the one you would like to clone this repository, preferably an easy-to-access one like the Desktop.
- This can be done very easily, just like the following examples:

In a machine with Linux or Windows PowerShell, you can use the terminal, by typing the following: 

```
cd directory_name
```
- Next, you can create a new directory, that will hold the programs you download, using the following command:

```
mkdir directory_name
```
- After that, I recommend you make a Python virtual environment with the following command:

```
python<version> -m venv <virtual-environment-name>
```
Make sure you include the version of Python you have and the name you would like your virtual environment to have.

- Next, you can copy and paste the following commands into your terminal in the same order they are written.
- Clone the repository

```bash
git clone https://github.com/Giova1016/CocktailBuddyAppDownload.git
```
- Install the required dependencies

```bash
pip install -r requirements.txt
```
- Lastly, you can run the .py file containing the code for one of the cryptographic algorithms mentioned in the [About](#about) section.
- Here is an example of how to run it.
```python
python<version> <program_name>.py

// Example
python LFSR.py
```
