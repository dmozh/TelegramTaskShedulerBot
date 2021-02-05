#this file have util function
from urllib.parse import unquote
import json


def get_params(url: str):
    """
    Get params from url
    :param url: str url
    :return: dict all params
    """
    params = {}
    symbols = ['{',
               '}',
               '[',
               ']',
               '(',
               ')',
               "'",
               '"',
               '`',
               '~',
               ',',
               ';',
               ':',
               '.',
               '<',
               '>',
               '!',
               '?']

    def replacing(param_value: str):
        param_value = unquote(param_value)
        for symbol in symbols:
            param_value = param_value.replace("symb", "")
        return param_value

    query_string = url.split('?')[1]
    params_list = query_string.split("&")
    for item in params_list:
        key, value = item.split('=')
        params[key] = replacing(value)

    return params


def replace_screen_symbols(text: str):
    """
    Function replacing all special symbols from text
    :param text: text
    :return: reformat text
    """
    symbols = {'&nbsp;': ' ', '&pound;': '£', '&euro;': '€', '&para;': '¶', '&sect;': '§', '&copy;': '©', '&reg;': '®',
               '&trade;': '™',
               '&deg;': '°', '&plusmn;': '±', '&frac14;': '¼', '&frac12;': '½', '&frac34;': '¾', '&times;': '×',
               '&divide;': '÷', '&fnof;': 'ƒ', '&Alpha;': 'Α', '&Beta;': 'Β', '&Gamma;': 'Γ', '&Delta;': 'Δ',
               '&Epsilon;': 'Ε', '&Zeta;': 'Ζ', '&Eta;': 'Η', '&Theta;': 'Θ', '&Iota;': 'Ι', '&Kappa;': 'Κ',
               '&Lambda;': 'Λ', '&Mu;': 'Μ', '&Nu;': 'Ν', '&Xi;': 'Ξ', '&Omicron;': 'Ο', '&Pi;': 'Π', '&Rho;': 'Ρ',
               '&Sigma;': 'Σ', '&Tau;': 'Τ', '&Upsilon;': 'Υ', '&Phi;': 'Φ', '&Chi;': 'Χ', '&Psi;': 'Ψ', '&Omega;': 'Ω',
               '&alpha;': 'α', '&beta;': 'β', '&gamma;': 'γ', '&delta;': 'δ', '&epsilon;': 'ε', '&zeta;': 'ζ',
               '&eta;': 'η', '&theta;': 'θ', '&iota;': 'ι', '&kappa;': 'κ', '&lambda;': 'λ', '&mu;': 'μ', '&nu;': 'ν',
               '&xi;': 'ξ', '&omicron;': 'ο', '&pi;': 'π', '&rho;': 'ρ', '&sigmaf;': 'ς', '&sigma;': 'σ', '&tau;': 'τ',
               '&upsilon;': 'υ', '&phi;': 'φ', '&chi;': 'χ', '&psi;': 'ψ', '&omega;': 'ω', '&larr;': '←', '&uarr;': '↑',
               '&rarr;': '→', '&darr;': '↓', '&harr;': '↔', '&spades;': '♠', '&clubs;': '♣', '&hearts;': '♥', '&diams;':
                   '♦', '&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&hellip;': '…', '&prime;': '′',
               '&Prime;': '″', '&ndash;': '–', '&mdash;': '—', '&lsquo;': '‘', '&rsquo;': '’', '&sbquo;': '‚',
               '&ldquo;': '“', '&rdquo;': '”', '&bdquo;': '„', '&laquo;': '«', '&raquo;': '»'}
    for key, value in symbols.items():
        text = text.replace(key, value)
    return text
