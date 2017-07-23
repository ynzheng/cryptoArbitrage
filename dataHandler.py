#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 21:52:07 2017

@author: garrettlee
"""
import kraken
import poloniex
import cryptopia
import bitfinex
import bittrex
import xbtce
import hitbtc
import time
import numpy as np
import pandas as pd
from twilio.rest import Client
import datetime

#information for messaging
sid, auth = 'ACab5ed88cf08f4d2df63791bfe06c47c6', 'e5cf603faa88be60621654aaf8ce2e92'
cli = Client(sid,auth)
myTwilioNumber, myCellPhone = '+13178544873', '+13176905477'

#Dictionaries for exchanges
bitfinexPairs = {'litecoin-bitcoin': 'ltcbtc', 'ethereum-bitcoin': 'ethbtc', 'ethereum classic-bitcoin': 'etcbtc', 'zcash-bitcoin': 'zecbtc', 'monero-bitcoin': 'xmrbtc', 'dash-bitcoin': 'dshbtc', 'bitconnect-bitcoin': 'bccbtc', 'ripple-bitcoin': 'xrpbtc', 'iota-bitcoin': 'iotbtc', 'iota-ethereum': 'ioteth', 'eos-bitcoin': 'eosbtc', 'eos-ethereum': 'eoseth'}
krakenPairs = {'dash-bitcoin': 'DASHXBT', 'eos-ethereum': 'EOSETH', 'eos-bitcoin': 'EOSXBT', 'gnosis-ethereum': 'GNOETH', 'gnosis-bitcoin': 'GNOXBT', 'ethereum classic-ethereum': 'XETCXETH', 'ethereum classic-bitcoin': 'XETCXXBT', 'ethereum-bitcoin': 'XETHXXBT', 'iconomi-ethereum': 'XICNXETH', 'iconomi-bitcoin': 'XICNXXBT', 'litecoin-bitcoin': 'XLTCXXBT', 'melon-ethereum': 'XMLNXETH', 'melon-bitcoin': 'XMLNXXBT', 'augur-ethereum': 'XREPXETH', 'augur-bitcoin': 'XREPXXBT', 'dogecoin-bitcoin': 'XXDGXXBT', 'stellar lumens-bitcoin': 'XXLMXXBT', 'monero-bitcoin': 'XXMRXXBT', 'ripple-bitcoin': 'XXRPXXBT', 'zcash-bitcoin': 'XZECXXBT'}
poloniexPairs = {'belacoin-bitcoin': 'BTC_BELA', 'bitcoin dark-bitcoin': 'BTC_BTCD', 'bitmark-bitcoin': 'BTC_BTM', 'bitshares-bitcoin': 'BTC_BTS', 'blackcoin-bitcoin': 'BTC_BLK', 'burst-bitcoin': 'BTC_BURST', 'bytecoin-bitcoin': 'BTC_BCN', 'clams-bitcoin': 'BTC_CLAM', 'dash-bitcoin': 'BTC_DASH', 'digibyte-bitcoin': 'BTC_DGB', 'dogecoin-bitcoin': 'BTC_DOGE', 'einsteinium': 'BTC_EMC2', 'floodingcoin-bitcoin': 'BTC_FLDC', 'florincoin-bitcoin': 'BTC_FLO', 'gamecredits-bitcoin': 'BTC_GAME', 'gridcoin-bitcoin': 'BTC_GRC', 'zcash-bitcoin': 'BTC_ZEC', 'ardor-bitcoin': 'BTC_ARDR', 'augur-bitcoin': 'BTC_REP', 'augur-ethereum': 'ETH_REP', 'augur-tether': 'USDT_REP', 'bitcoin plus-bitcoin': 'BTC_XBC', 'bitcrystals-bitcoin': 'BTC_BCY', 'counterparty-bitcoin': 'BTC_XCP', 'dash-tether': 'USDT_DASH', 'decred-bitcoin': 'BTC_DCR', 'dnotes-bitcoin': 'BTC_NOTE', 'ethereum classic-bitcoin': 'BTC_ETC', 'ethereum classic-ethereum': 'ETH_ETC', 'ethereum classic-tether': 'USDT_ETC', 'ethereum-bitcoin': 'BTC_ETH', 'ethereum-steem': 'ETH_STEEM', 'ethereum-tether': 'USDT_ETH', 'expanse-bitcoin': 'BTC_EXP', 'factom-bitcoin': 'BTC_FCT', 'gnosis-bitcoin': 'BTC_GNO', 'gnosis-ethereum': 'ETH_GNO', 'golem-bitcoin': 'BTC_GNT', 'golem-ethereum': 'ETH_GNT', 'huntercoin-bitcoin': 'BTC_HUC', 'lisk-bitcoin': 'BTC_LSK', 'list-ethereum': 'ETH_LSK', 'litecoin-bitcoin': 'BTC_LTC', 'litecoin-tether': 'USDT_LTC', 'maidsafecoin-bitcoin': 'BTC_MAID', 'monero-bitcoin': 'BTC_XMR', 'monero-tether': 'USDT_XMR', 'monero-zcash': 'XMR_ZEC', 'namecoin-bitcoin': 'BTC_NMC', 'nautiluscoin-bitcoin': 'BTC_NAUT', 'navcoin-bitcoin': 'BTC_NAV', 'nem-bitcoin': 'BTC_XEM', 'neoscoin': 'BTC_NEOS', 'nexium-bitcoin': 'BTC_NXC', 'nxt-bitcoin': 'BTC_NXT', 'nxt-tether': 'USDT_NXT', 'omni-bitcoin': 'BTC_OMNI', 'pascalcoin-bitcoin': 'BTC_PASC', 'peercoin-bitcoin': 'BTC_PPC', 'pinkcoin-bitcoin': 'BTC_PINK', 'potcoin-bitcoin': 'BTC_POT', 'primecoin-bitcoin': 'BTC_XPM', 'radium-bitcoin': 'BTC_RADS', 'riecoin-bitcoin': 'BTC_RIC', 'ripple-bitcoin': 'BTC_XRP', 'ripple-tether': 'USDT_XRP', 'siacoin-bitcoin': 'BTC_SC', 'steem-bitcoin': 'BTC_STEEM', 'storjcoin x-bitcoin': 'BTC_SJCX', 'stratus-bitcoin': 'BTC_STRAT', 'synereo-bitcoin': 'BTC_AMP', 'syscoin-bitcoin': 'BTC_SYS', 'tether-bitcoin': 'USDT_BTC', 'vcash-bitcoin': 'BTC_XVC', 'vericoin-bitcoin': 'BTC_VRC', 'vertcoin-bitcoin': 'BTC_VTC', 'viacoin-bitcoin': 'BTC_VIA', 'zcash-ethereum': 'ETH_ZEC', 'zcash-tether': 'USDT_ZEC'}
cryptopiaPairs = {'1337-bitcoin': '1337_BTC', '23skidoo-bitcoin': 'CHAO_BTC', '42-coin-bitcoin': '42_BTC', '808-bitcoin': '808_BTC', '8bit-bitcoin': '8BIT_BTC', 'acoin-bitcoin': 'ACOIN_BTC', 'alexandrite-bitcoin': 'ALEX_BTC', 'allion-bitcoin': 'ALL_BTC', 'altcoin-bitcoin': 'ALT_BTC', 'anarchistsprime-bitcoin': 'ACP_BTC', 'animecoin-bitcoin': 'ANI_BTC', 'aquariuscoin-bitcoin': 'ARCO_BTC', 'arcticcoin-bitcoin': 'ARC_BTC', 'argentum-bitcoin': 'ARG_BTC', 'arguscoin-bitcoin': 'ARGUS_BTC', 'aricoin-bitcoin': 'ARI_BTC', 'ark-bitcoin': 'ARK_BTC', 'ark-tether': 'ARK_USDT', 'asiacoin-bitcoin': 'AC_BTC', 'atmos-bitcoin': 'ATMS_BTC', 'atomiccoin-bitcoin': 'ATOM_BTC', 'audiocoin-bitcoin': 'ADC_BTC', 'augur-bitcoin': 'REP_BTC', 'auroracoin-bitcoin': 'AUR_BTC', 'aurumcoin-bitcoin': 'AU_BTC', 'b3 coin-bitcoin': 'B3_BTC', 'b@nkcoin-bitcoin': 'B@_BTC', 'bata-bitcoin': 'BTA_BTC', 'beachcoin-bitcoin': 'SAND_BTC', 'beatcoin-bitcoin': 'XBTS_BTC', 'beavercoin-bitcoin': 'BVC_BTC', 'beezercoin-bitcoin': 'BEEZ_BTC', 'benjirolls-bitcoin': 'BENJI_BTC', 'berncash-bitcoin': 'BERN_BTC', 'bestchain-bitcoin': 'BEST_BTC', 'bikercoin-bitcoin': 'BIC_BTC', 'bipcoin-bitcoin': 'BIP_BTC', 'bitbar-bitcoin': 'BTB_BTC', 'bitbean-bitcoin': 'BITB_BTC', 'bitcedi-bitcoin': 'BXC_BTC', 'bitcoal-bitcoin': 'COAL_BTC', 'bitcoin scrypt-bitcoin': 'BTCS_BTC', 'bitcoin scrypt-dogecoin': 'BTCS_DOGE', 'bitcoin scrypt-litecoin': 'BTCS_LTC', 'bitcoin-nzed': 'BTC_NZDT', 'bitcoin-tether': 'BTC_USDT', 'bitcoindark-bitcoin': 'BTCD_BTC', 'bitcoindark-dogecoin': 'BTCD_DOGE', 'bitcoindark-litecoin': 'BTCD_LTC', 'bitcoinfast-bitcoin': 'BCF_BTC', 'bitcoinfast-dogecoin': 'BCF_DOGE', 'bitcoinfast-litecoin': 'BCF_LTC', 'bitcoinplus-bitcoin': 'XBC_BTC', 'bitcoinplus-dogecoin': 'XBC_DOGE', 'bitcoinplus-litecoin': 'XBC_LTC', 'bitcore-bitcoin': 'BTX_BTC', 'bitgem-bitcoin': 'BTG_BTC', 'bitsend-bitcoin': 'BSD_BTC', 'bitsend-tether': 'BSD_USDT', 'bitstar-bitcoin': 'BITS_BTC', 'blackcoin-bitcoin': 'BLK_BTC', 'blakecoin-bitcoin': 'BLC_BTC', 'bnrtxcoin-bitcoin': 'BNX_BTC', 'bolivarcoin-bitcoin': 'BOLI_BTC', 'boolberry-bitcoin': 'BBR_BTC', 'bottlecaps-bitcoin': 'CAP_BTC', 'bumbacoin-bitcoin': 'BUMBA_BTC', 'bvbcoin-bitcoin': 'BVB_BTC', 'byteball-bitcoin': 'GBYTE_BTC', 'bytecoin-bitcoin': 'BCN_BTC', 'c-bit-bitcoin': 'XCT_BTC', 'cachecoin-bitcoin': 'CACH_BTC', 'canada ecoin-bitcoin': 'CDN_BTC', 'cannabiscoin-bitcoin': 'CANN_BTC', 'cannacoin-bitcoin': 'CCN_BTC', 'careercoin-bitcoin': 'CAR_BTC', 'casinocoin-bitcoin': 'CSC_BTC', 'catcoin-bitcoin': 'CAT_BTC', 'cbdcrystals-bitcoin': 'CBD_BTC', 'chaincoin-bitcoin': 'CHC_BTC', 'chaincoin-tether': 'CHC_USDT', 'chancoin-bitcoin': '4CHN_BTC', 'chesscoin-bitcoin': 'CHESS_BTC', 'chronoscoin-bitcoin': 'CRX_BTC', 'clamcoin-bitcoin': 'CLAM_BTC', 'cloakcoin-bitcoin': 'CLOAK_BTC', 'cloudcoin-bitcoin': 'CDC_BTC', 'coffeecoin-bitcoin': 'CFC_BTC', 'coin2-bitcoin': 'C2_BTC', 'coino-bitcoin': 'CNO_BTC', 'coinonat-bitcoin': 'CXT_BTC', 'cometcoin-bitcoin': 'CMT_BTC', 'compucoin-bitcoin': 'CPN_BTC', 'condensate-bitcoin': 'RAIN_BTC', 'conquestcoin-bitcoin': 'CQST_BTC', 'coolindarkcoin-bitcoin': 'CC_BTC', 'corgicoin-bitcoin': 'CORG_BTC', 'crave-bitcoin': 'CRAVE_BTC', 'creatio-bitcoin': 'XCRE_BTC', 'creativecoin-bitcoin': 'CREA_BTC', 'cryptcoin-bitcoin': 'CRYPT_BTC', 'cryptobullion-bitcoin': 'CBX_BTC', 'cryptoforecast-bitcoin': 'CFT_BTC', 'cryptojacks-bitcoin': 'CJ_BTC', 'cryptoping-bitcoin': 'PING_BTC', 'cthulhu offerings-bitcoin': 'OFF_BTC', 'cubits-bitcoin': 'QBT_BTC', 'dark-bitcoin': 'DARK_BTC', 'darsek-bitcoin': 'KED_BTC', 'dash-bitcoin': 'DASH_BTC', 'dash-tether': 'DASH_USDT', 'dashcoin-bitcoin': 'DSH_BTC', 'daxxcoin-bitcoin': 'DAXX_BTC', 'decred-bitcoin': 'DCR_BTC', 'decred-tether': 'DCR_USDT', 'deutsche emark-bitcoin': 'DEM_BTC', 'dibcoin -bitcoin': 'DIBC_BTC', 'digibyte-bitcoin': 'DGB_BTC', 'digitalcoin-bitcoin': 'DGC_BTC', 'digitalmoneybits-bitcoin': 'DMB_BTC', 'dinastycoin-bitcoin': 'DCY_BTC', 'dnotes-bitcoin': 'NOTE_BTC', 'dobbscoin-bitcoin': 'BOB_BTC', 'dogecoin-bitcoin': 'DOGE_BTC', 'dogecoin-tether': 'DOGE_USDT', 'donationcoin-bitcoin': 'DON_BTC', 'dotcoin-bitcoin': 'DOT_BTC', 'dotcoin-tether': 'DOT_USDT', 'duckduckcoin-bitcoin': 'DUCK_BTC', 'e-gulden-bitcoin': 'EFL_BTC', 'eclipse-bitcoin': 'EC_BTC', 'ecobit-bitcoin': 'ECOB_BTC', 'ecocoin-bitcoin': 'ECO_BTC', 'edrcoin-bitcoin': 'EDRC_BTC', 'educoinv-bitcoin': 'EDC_BTC', 'einsteinium-bitcoin': 'EMC2_BTC', 'elacoin-bitcoin': 'ELC_BTC', 'elysium-bitcoin': 'ELS_BTC', 'embargocoin-bitcoin': 'EBG_BTC', 'embercoin-bitcoin': 'EMB_BTC', 'emerald crypto-bitcoin': 'EMD_BTC', 'emercoin-bitcoin': 'EMC_BTC', 'equitrader-bitcoin': 'EQT_BTC', 'eryllium-bitcoin': 'ERY_BTC', 'ethbits-bitcoin': 'ETB_BTC', 'ethereum classic-bitcoin': 'ETC_BTC', 'ethereum classic-dogecoin': 'ETC_DOGE', 'ethereum classic-litecoin': 'ETC_LTC', 'ethereum classic-nzed': 'ETC_NZDT', 'ethereum classic-tether': 'ETC_USDT', 'ethereum-bitcoin': 'ETH_BTC', 'ethereum-dogecoin': 'ETH_DOGE', 'ethereum-litecoin': 'ETH_LTC', 'ethereum-nzed': 'ETH_NZDT', 'ethereum-tether': 'ETH_USDT', 'eurocoin-bitcoin': 'EUC_BTC', 'evergreencoin-bitcoin': 'EGC_BTC', 'evilcoin-bitcoin': 'EVIL_BTC', 'evotion-bitcoin': 'EVO_BTC', 'expanse-bitcoin': 'EXP_BTC', 'facilecoin-bitcoin': 'FCN_BTC', 'factom-bitcoin': 'FCT_BTC', 'famecoin-bitcoin': 'FAME_BTC', 'fastcoin-bitcoin': 'FST_BTC', 'fazzcoin-bitcoin': 'FAZZ_BTC', 'feathercoin-bitcoin': 'FTC_BTC', 'fireflycoin-bitcoin': 'FFC_BTC', 'fireroostercoin-bitcoin': 'FRC_BTC', 'flash-bitcoin': 'FLASH_BTC', 'flaxscript-bitcoin': 'FLAX_BTC', 'fluttercoin-bitcoin': 'FLT_BTC', 'fonziecoin-bitcoin': 'FONZ_BTC', 'footycash-bitcoin': 'FOOT_BTC', 'francs-bitcoin': 'FRN_BTC', 'fuelcoin-bitcoin': 'FUEL_BTC', 'fujicoin-bitcoin': 'FJC_BTC', 'fuzzballs-bitcoin': 'FUZZ_BTC', 'gaiacoin-bitcoin': 'GAIA_BTC', 'gamecredits-bitcoin': 'GAME_BTC', 'gameunits-bitcoin': 'UNITS_BTC', 'gapcoin-bitcoin': 'GAP_BTC', 'gaycoin-bitcoin': 'GAY_BTC', 'geertcoin-bitcoin': 'GEERT_BTC', 'geocoin-bitcoin': 'GEO_BTC', 'globalboost-y-bitcoin': 'BSTY_BTC', 'gnosis-bitcoin': 'GNO_BTC', 'goldcoin-bitcoin': 'GLD_BTC', 'goldpieces-bitcoin': 'GP_BTC', 'goldpressedlatinum -bitcoin': 'GPL_BTC', 'goldreserve-bitcoin': 'XGR_BTC', 'golem-bitcoin': 'GNT_BTC', 'gpucoin-bitcoin': 'GPU_BTC', 'granite-bitcoin': 'GRN_BTC', 'groestlcoin-bitcoin': 'GRS_BTC', 'growthcoin-bitcoin': 'GRW_BTC', 'guncoin-bitcoin': 'GUN_BTC', 'halcyon-bitcoin': 'HAL_BTC', 'hexxcoin-bitcoin': 'HXX_BTC', 'hobonickels-bitcoin': 'HBN_BTC', 'hush-bitcoin': 'HUSH_BTC', 'hush-tether': 'HUSH_USDT', 'hyperstake-bitcoin': 'HYP_BTC', 'i0coin-bitcoin': 'I0C_BTC', 'icebergcoin-bitcoin': 'ICB_BTC', 'icobid-bitcoin': 'ICOB_BTC', 'impeachcoin-bitcoin': 'IMPCH_BTC', 'incakoin-bitcoin': 'NKA_BTC', 'incent-bitcoin': 'INCNT_BTC', 'incoin-bitcoin': 'IN_BTC', 'independent money system-bitcoin': 'IMS_BTC', 'influxcoin-bitcoin': 'INFX_BTC', 'inpay-bitcoin': 'INPAY_BTC', 'inpay-tether': 'INPAY_USDT', 'insane-bitcoin': 'INSN_BTC', 'iou1-bitcoin': 'IOU_BTC', 'irishcoin-bitcoin': 'IRL_BTC', 'iticoin-bitcoin': 'ITI_BTC', 'ivugeocoin-bitcoin': 'IEC_BTC', 'ixcoin-bitcoin': 'IXC_BTC', 'janecoin-bitcoin': 'JANE_BTC', 'jetcoin-bitcoin': 'JET_BTC', 'joulecoin-bitcoin': 'XJO_BTC', 'jyn erso-bitcoin': 'ERSO_BTC', 'karbowanec-bitcoin': 'KRB_BTC', 'kashcoin-bitcoin': 'KASH_BTC', 'kayi-bitcoin': 'KAYI_BTC', 'klondikecoin-bitcoin': 'KDC_BTC', 'kobocoin-bitcoin': 'KOBO_BTC', 'komodo-bitcoin': 'KMD_BTC', 'kurrent-bitcoin': 'KURT_BTC', 'kushcoin-bitcoin': 'KUSH_BTC', 'ladacoin-bitcoin': 'LDC_BTC', 'lanacoin-bitcoin': 'LANA_BTC', 'lbry credits-bitcoin': 'LBC_BTC', 'le pen coin-bitcoin': 'LEPEN_BTC', 'lemoncoin-bitcoin': 'LEMON_BTC', 'lindacoin-bitcoin': 'LINDA_BTC', 'litebar-bitcoin': 'LTB_BTC', 'litecoin-bitcoin': 'LTC_BTC', 'litecoin-tether': 'LTC_USDT', 'litedoge-bitcoin': 'LDOGE_BTC', 'lithiumcoin-bitcoin': 'LIT_BTC', 'lizi-bitcoin': 'LIZI_BTC', 'machinecoin-bitcoin': 'MAC_BTC', 'macron-bitcoin': 'MCRN_BTC', 'magi-bitcoin': 'XMG_BTC', 'magnetcoin-bitcoin': 'MAGN_BTC', 'maidsafecoin-bitcoin': 'MAID_BTC', 'marijuanacoin-bitcoin': 'MAR_BTC', 'mars-bitcoin': 'MARS_BTC', 'marxcoin-bitcoin': 'MARX_BTC', 'mazacoin-bitcoin': 'MZC_BTC', 'megacoin-bitcoin': 'MEC_BTC', 'melite-bitcoin': 'MLITE_BTC', 'mercury-bitcoin': 'MER_BTC', 'metalmusiccoin-bitcoin': 'MTLMC_BTC', 'minereum-bitcoin': 'MNE_BTC', 'mineum-bitcoin': 'MNM_BTC', 'mintcoin-bitcoin': 'MINT_BTC', 'moin-bitcoin': 'MOIN_BTC', 'mojocoin-bitcoin': 'MOJO_BTC', 'monero-bitcoin': 'XMR_BTC', 'monero-tether': 'XMR_USDT', 'money-bitcoin': '$$$_BTC', 'motocoin-bitcoin': 'MOTO_BTC', 'musicoin-bitcoin': 'MUSIC_BTC', 'mustangcoin-bitcoin': 'MST_BTC', 'myriad-bitcoin': 'XMY_BTC', 'namecoin-bitcoin': 'NMC_BTC', 'navcoin-bitcoin': 'NAV_BTC', 'navcoin-tether': 'NAV_USDT', 'netcoin-bitcoin': 'NET_BTC', 'netko-bitcoin': 'NETKO_BTC', 'neutron-bitcoin': 'NTRN_BTC', 'nevacoin-bitcoin': 'NEVA_BTC', 'neweconomymovement-bitcoin': 'XEM_BTC', 'nexus-bitcoin': 'NXS_BTC', 'noblecoin-bitcoin': 'NOBL_BTC', 'novacoin-bitcoin': 'NVC_BTC', 'nubits-bitcoin': 'USNBT_BTC', 'nushares-bitcoin': 'NSR_BTC', 'nyancoin-bitcoin': 'NYAN_BTC', 'nzed-tether': 'NZDT_USDT', 'octocoin-bitcoin': '888_BTC', 'okcash-bitcoin': 'OK_BTC', 'om-bitcoin': 'OOO_BTC', 'opalcoin-bitcoin': 'OPAL_BTC', 'open source coin-bitcoin': 'OSC_BTC', 'orbitcoin-bitcoin': 'ORB_BTC', 'orbitcoin-dogecoin': 'ORB_DOGE', 'orbitcoin-litecoin': 'ORB_LTC', 'pakcoin-bitcoin': 'PAK_BTC', 'parallelcoin-bitcoin': 'DUO_BTC', 'pascalcoin-bitcoin': 'PASC_BTC', 'pascallite-bitcoin': 'PASL_BTC', 'paycon-bitcoin': 'CON_BTC', 'peercoin-bitcoin': 'PPC_BTC', 'pepecoin-bitcoin': 'PEPE_BTC', 'pesetacoin-bitcoin': 'PTC_BTC', 'petrodollar-bitcoin': 'XPD_BTC', 'philosopherstone-bitcoin': 'PHS_BTC', 'phoenixcoin-bitcoin': 'PXC_BTC', 'piggycoin-bitcoin': 'PIGGY_BTC', 'pinkcoin-bitcoin': 'PINK_BTC', 'pivx-bitcoin': 'PIVX_BTC', 'pivx-tether': 'PIVX_USDT', 'polcoin-bitcoin': 'PLC_BTC', 'polishcoin-bitcoin': 'PCC_BTC', 'postcoin-bitcoin': 'POST_BTC', 'poswallet-bitcoin': 'POSW_BTC', 'potcoin-bitcoin': 'POT_BTC', 'prime-xi-bitcoin': 'PXI_BTC', 'primecoin-bitcoin': 'XPM_BTC', 'procurrency-bitcoin': 'PROC_BTC', 'prototanium-bitcoin': 'PR_BTC', 'purevidz-bitcoin': 'VIDZ_BTC', 'putincoin-bitcoin': 'PUT_BTC', 'quark-bitcoin': 'QRK_BTC', 'quatloo-bitcoin': 'QTL_BTC', 'qubitcoin-bitcoin': 'Q2C_BTC', 'qubitcoin-dogecoin': 'Q2C_DOGE', 'qubitcoin-litecoin': 'Q2C_LTC', 'rabbitcoin-dogecoin': 'RBBT_DOGE', 'rabbitcoin-litecoin': 'RBBT_LTC', 'ratecoin-bitcoin': 'XRA_BTC', 'redcoin-bitcoin': 'RED_BTC', 'reddcoin-bitcoin': 'RDD_BTC', 'renoscoin-bitcoin': 'RNS_BTC', 'revolvercoin-bitcoin': 'XRE_BTC', 'rimbit-bitcoin': 'RBT_BTC', 'ripto bux-bitcoin': 'RBX_BTC', 'ronpaulcoin-bitcoin': 'RPC_BTC', 'rubycoin-bitcoin': 'RBY_BTC', 'russiacoin-bitcoin': 'RC_BTC', 'safeexchangecoin-bitcoin': 'SAFEX_BTC', 'sakuracoin-bitcoin': 'SKR_BTC', 'sativacoin-bitcoin': 'STV_BTC', 'scorecoin-bitcoin': 'SCORE_BTC', 'selencoin-bitcoin': 'SEL_BTC', 'sexcoin-bitcoin': 'SXC_BTC', 'shacoin2-bitcoin': 'SHA_BTC', 'sharkcoin-bitcoin': 'SAK_BTC', 'siacoin-bitcoin': 'SC_BTC', 'siberianchervonets-bitcoin': 'SIB_BTC', 'skeincoin-bitcoin': 'SKC_BTC', 'skycoin-bitcoin': 'SKY_BTC', 'skycoin-tether': 'SKY_USDT', 'smartcoin-bitcoin': 'SMC_BTC', 'solarflarecoin-bitcoin': 'SFC_BTC', 'solaris-bitcoin': 'XLR_BTC', 'songcoin-bitcoin': 'SONG_BTC', 'sooncoin-bitcoin': 'SOON_BTC', 'spacecoin-bitcoin': 'SPACE_BTC', 'spectre-bitcoin': 'XSPEC_BTC', 'spots-bitcoin': 'SPT_BTC', 'squallcoin-bitcoin': 'SQL_BTC', 'stablecoin-bitcoin': 'SBC_BTC', 'startcoin-bitcoin': 'START_BTC', 'sterlingcoin-bitcoin': 'SLG_BTC', 'stoptrumpcoin-bitcoin': 'STC_BTC', 'stratis-bitcoin': 'STRAT_BTC', 'suicidecoin-bitcoin': 'SCD_BTC', 'sumokoin-bitcoin': 'SUMO_BTC', 'swagbucks-bitcoin': 'BUCKS_BTC', 'swingcoin-bitcoin': 'SWING_BTC', 'syndicate-bitcoin': 'SYNX_BTC', 'synereo amp-bitcoin': 'AMP_BTC', 'tajcoin-bitcoin': 'TAJ_BTC', 'tattoocoin-bitcoin': 'TSE_BTC', 'tekcoin-bitcoin': 'TEK_BTC', 'terracoin-bitcoin': 'TRC_BTC', 'terranova-bitcoin': 'TER_BTC', 'teslacoin-bitcoin': 'TES_BTC', 'thechiefcoin-bitcoin': 'CHIEF_BTC', 'tigercoin-bitcoin': 'TGC_BTC', 'titcoin-bitcoin': 'TIT_BTC', 'tittiecoin-bitcoin': 'TTC_BTC', 'toacoin-bitcoin': 'TOA_BTC', 'topcoin-bitcoin': 'TOP_BTC', 'torcoin-bitcoin': 'TOR_BTC', 'transfercoin-bitcoin': 'TX_BTC', 'triangles-bitcoin': 'TRI_BTC', 'truckcoin-bitcoin': 'TRK_BTC', 'trueinvestmentcoin-bitcoin': 'TIC_BTC', 'trumpcoin-bitcoin': 'TRUMP_BTC', 'ubiq-bitcoin': 'UBQ_BTC', 'ultracoin-bitcoin': 'UTC_BTC', 'unbreakablecoin-bitcoin': 'UNB_BTC', 'unicoin-bitcoin': 'UNIC_BTC', 'unify-bitcoin': 'UNIFY_BTC', 'unitus-bitcoin': 'UIS_BTC', 'universalmolecule-bitcoin': 'UMO_BTC', 'unobtanium-bitcoin': 'UNO_BTC', 'unobtanium-tether': 'UNO_USDT', 'ur-bitcoin': 'UR_BTC', 'vadercorpcoin-bitcoin': 'VCC_BTC', 'verge-bitcoin': 'XVG_BTC', 'vericoin-bitcoin': 'VRC_BTC', 'verium-bitcoin': 'VRM_BTC', 'version-bitcoin': 'V_BTC', 'visio-bitcoin': 'VISIO_BTC', 'voise-bitcoin': 'VSM_BTC', 'warcoin-bitcoin': 'WRC_BTC', 'waves-bitcoin': 'WAVES_BTC', 'waves-tether': 'WAVES_USDT', 'wayawolfcoin-bitcoin': 'WW_BTC', 'wearesatoshi-bitcoin': 'WSX_BTC', 'wirelesscoin-bitcoin': 'WLC_BTC', 'worldcoin-bitcoin': 'WDC_BTC', 'xtrabytes-bitcoin': 'XBY_BTC', 'yobitcoin-bitcoin': 'YOVI_BTC', 'yobitcoin-dogecoin': 'YOVI_DOGE', 'yobitcoin-litecoin': 'YOVI_LTC', 'zcash-bitcoin': 'ZEC_BTC', 'zcash-tether': 'ZEC_USDT', 'zclassic-bitcoin': 'ZCL_BTC', 'zcoin-bitcoin': 'XZC_BTC', 'zeitcoin-bitcoin': 'ZEIT_BTC', 'zero-bitcoin': 'ZER_BTC', 'zetacoin-bitcoin': 'ZET_BTC', 'zoin-bitcoin': 'ZOI_BTC', 'zsecoin-bitcoin': 'ZSE_BTC'}
bittrexPairs = {'bitcoin-bitcny': 'BITCNY-BTC', 'firstblood-bitcoin': 'BTC-1ST', '2give-bitcoin': 'BTC-2GIVE', 'artbyte-bitcoin': 'BTC-ABY', 'adtoken-bitcoin': 'BTC-ADT', 'adex-bitcoin': 'BTC-ADX', 'aeon-bitcoin': 'BTC-AEON', 'idni agoras-bitcoin': 'BTC-AGRS', 'synereoamp-bitcoin': 'BTC-AMP', 'antshares-bitcoin': 'BTC-ANS', 'aragon-bitcoin': 'BTC-ANT', 'apx-bitcoin': 'BTC-APX', 'ardor-bitcoin': 'BTC-ARDR', 'ark-bitcoin': 'BTC-ARK', 'auroracoin-bitcoin': 'BTC-AUR', 'basic attention token-bitcoin': 'BTC-BAT', 'bitbay-bitcoin': 'BTC-BAY', 'bitcrystals-bitcoin': 'BTC-BCY', 'bitbean-bitcoin': 'BTC-BITB', 'blitzcash-bitcoin': 'BTC-BLITZ', 'blackcoin-bitcoin': 'BTC-BLK', 'blocknet-bitcoin': 'BTC-BLOCK', 'bancor-bitcoin': 'BTC-BNT', 'breakout-bitcoin': 'BTC-BRK', 'breakout stake-bitcoin': 'BTC-BRX', 'bitsend-bitcoin': 'BTC-BSD', 'bata-bitcoin': 'BTC-BTA', 'bitcoindark-bitcoin': 'BTC-BTCD', 'bitshares-bitcoin': 'BTC-BTS', 'burst-bitcoin': 'BTC-BURST', 'bytecent-bitcoin': 'BTC-BYC', 'cannabiscoin-bitcoin': 'BTC-CANN', 'cofound.it-bitcoin': 'BTC-CFI', 'clams-bitcoin': 'BTC-CLAM', 'cloakcoin-bitcoin': 'BTC-CLOAK', 'clubcoin-bitcoin': 'BTC-CLUB', 'circuits of value-bitcoin': 'BTC-COVAL', 'capricoin-bitcoin': 'BTC-CPC', 'creditbit-bitcoin': 'BTC-CRB', 'crown-bitcoin': 'BTC-CRW', 'curecoin-bitcoin': 'BTC-CURE', 'darcrus-bitcoin': 'BTC-DAR', 'dash-bitcoin': 'BTC-DASH', 'decred-bitcoin': 'BTC-DCR', 'decent-bitcoin': 'BTC-DCT', 'digibyte-bitcoin': 'BTC-DGB', 'digix dao-bitcoin': 'BTC-DGD', 'diamond-bitcoin': 'BTC-DMD', 'dogecoin-bitcoin': 'BTC-DOGE', 'dopecoin-bitcoin': 'BTC-DOPE', 'dt token-bitcoin': 'BTC-DRACO', 'databits-bitcoin': 'BTC-DTB', 'dynamic-bitcoin': 'BTC-DYN', 'eboost-bitcoin': 'BTC-EBST', 'edgeless-bitcoin': 'BTC-EDG', 'electronicgulden-bitcoin': 'BTC-EFL', 'evergreencoin-bitcoin': 'BTC-EGC', 'emercoin-bitcoin': 'BTC-EMC', 'einsteinium-bitcoin': 'BTC-EMC2', 'energycoin-bitcoin': 'BTC-ENRG', 'europecoin-bitcoin': 'BTC-ERC', 'ethereum classic-bitcoin': 'BTC-ETC', 'ethereum-bitcoin': 'BTC-ETH', 'exclusivecoin-bitcoin': 'BTC-EXCL', 'expanse-bitcoin': 'BTC-EXP', 'faircoin-bitcoin': 'BTC-FAIR', 'factom-bitcoin': 'BTC-FCT', 'foldingcoin-bitcoin': 'BTC-FLDC', 'florin-bitcoin': 'BTC-FLO', 'feathercoin-bitcoin': 'BTC-FTC', 'funfair-bitcoin': 'BTC-FUN', 'gambit-bitcoin': 'BTC-GAM', 'gamecredits-bitcoin': 'BTC-GAME', 'gbg-bitcoin': 'BTC-GBG', 'byteball-bitcoin': 'BTC-GBYTE', 'globalcurrencyreserve-bitcoin': 'BTC-GCR', 'geocoin-bitcoin': 'BTC-GEO', 'goldcoin-bitcoin': 'BTC-GLD', 'gnosis-bitcoin': 'BTC-GNO', 'golem-bitcoin': 'BTC-GNT', 'golos-bitcoin': 'BTC-GOLOS', 'gridcoin-bitcoin': 'BTC-GRC', 'groestlcoin-bitcoin': 'BTC-GRS', 'guppy-bitcoin': 'BTC-GUP', 'hackergold-bitcoin': 'BTC-HKG', 'humaniq-bitcoin': 'BTC-HMQ', 'incent-bitcoin': 'BTC-INCNT', 'influxcoin-bitcoin': 'BTC-INFX', 'i/ocoin-bitcoin': 'BTC-IOC', 'ion-bitcoin': 'BTC-ION', 'internet of people-bitcoin': 'BTC-IOP', 'komodo-bitcoin': 'BTC-KMD', 'korecoin-bitcoin': 'BTC-KORE', 'lbry credits-bitcoin': 'BTC-LBC', 'legends-bitcoin': 'BTC-LGD', 'lomocoin-bitcoin': 'BTC-LMC', 'lisk-bitcoin': 'BTC-LSK', 'litecoin-bitcoin': 'BTC-LTC', 'lunyr-bitcoin': 'BTC-LUN', 'maidsafecoin-bitcoin': 'BTC-MAID', 'monaco-bitcoin': 'BTC-MCO', 'memetic-bitcoin': 'BTC-MEME', 'melon-bitcoin': 'BTC-MLN', 'monacoin-bitcoin': 'BTC-MONA', 'metal-bitcoin': 'BTC-MTL', 'monetaryunit-bitcoin': 'BTC-MUE', 'musicoin-bitcoin': 'BTC-MUSIC', 'myriadcoin-bitcoin': 'BTC-MYR', 'mysterium-bitcoin': 'BTC-MYST', 'nautiluscoin-bitcoin': 'BTC-NAUT', 'navcoin-bitcoin': 'BTC-NAV', 'nubits-bitcoin': 'BTC-NBT', 'neoscoin-bitcoin': 'BTC-NEOS', 'gulden-bitcoin': 'BTC-NLG', 'numeraire-bitcoin': 'BTC-NMR', 'nexium-bitcoin': 'BTC-NXC', 'nexus-bitcoin': 'BTC-NXS', 'nxt-bitcoin': 'BTC-NXT', 'okcash-bitcoin': 'BTC-OK', 'omnicoin-bitcoin': 'BTC-OMNI', 'tenx pay token-bitcoin': 'BTC-PAY', 'project decorum-bitcoin': 'BTC-PDC', 'pinkcoin-bitcoin': 'BTC-PINK', 'pivx-bitcoin': 'BTC-PIVX', 'parkbyte-bitcoin': 'BTC-PKB', 'potcoin-bitcoin': 'BTC-POT', 'peercoin-bitcoin': 'BTC-PPC', 'pesetacoin -bitcoin': 'BTC-PTC', 'patientory-bitcoin': 'BTC-PTOY', 'quantum resistant ledger-bitcoin': 'BTC-QRL', 'qwark-bitcoin': 'BTC-QWARK', 'radium-bitcoin': 'BTC-RADS', 'rubycoin-bitcoin': 'BTC-RBY', 'reddcoin-bitcoin': 'BTC-RDD', 'augur-bitcoin': 'BTC-REP', 'rise-bitcoin': 'BTC-RISE', 'iex.ec-bitcoin': 'BTC-RLC', 'steemdollars-bitcoin': 'BTC-SBD', 'siacoin-bitcoin': 'BTC-SC', 'safeexchangecoin-bitcoin': 'BTC-SEC', 'sequence-bitcoin': 'BTC-SEQ', 'shift-bitcoin': 'BTC-SHIFT', 'siberian chervonets-bitcoin': 'BTC-SIB', 'solarcoin-bitcoin': 'BTC-SLR', 'salus-bitcoin': 'BTC-SLS', 'singulardtv-bitcoin': 'BTC-SNGLS', 'synergy-bitcoin': 'BTC-SNRG', 'status network token-bitcoin': 'BTC-SNT', 'sphere-bitcoin': 'BTC-SPHR', 'spreadcoin-bitcoin': 'BTC-SPR', 'startcoin-bitcoin': 'BTC-START', 'steem-bitcoin': 'BTC-STEEM', 'storj-bitcoin': 'BTC-STORJ', 'stratis-bitcoin': 'BTC-STRAT', 'bitswift-bitcoin': 'BTC-SWIFT', 'swarm city token-bitcoin': 'BTC-SWT', 'syndicate-bitcoin': 'BTC-SYNX', 'syscoin-bitcoin': 'BTC-SYS', 'hempcoin-bitcoin': 'BTC-THC', 'chronobank time-bitcoin': 'BTC-TIME', 'tokencard-bitcoin': 'BTC-TKN', 'tokes-bitcoin': 'BTC-TKS', 'trig token-bitcoin': 'BTC-TRIG', 'trustcoin-bitcoin': 'BTC-TRST', 'trustplus-bitcoin': 'BTC-TRUST', 'transfercoin-bitcoin': 'BTC-TX', 'ubiq-bitcoin': 'BTC-UBQ', 'unbreakablecoin-bitcoin': 'BTC-UNB', 'unobtanium-bitcoin': 'BTC-UNO', 'viacoin-bitcoin': 'BTC-VIA', 'voxels-bitcoin': 'BTC-VOX', 'vericoin-bitcoin': 'BTC-VRC', 'verium-bitcoin': 'BTC-VRM', 'vertcoin-bitcoin': 'BTC-VTC', 'vtorrent-bitcoin': 'BTC-VTR', 'waves-bitcoin': 'BTC-WAVES', 'wings dao-bitcoin': 'BTC-WINGS', 'xaurum-bitcoin': 'BTC-XAUR', 'boolberry-bitcoin': 'BTC-XBB', 'counterparty-bitcoin': 'BTC-XCP', 'digitalnote-bitcoin': 'BTC-XDN', 'elastic-bitcoin': 'BTC-XEL', 'neweconomymovement-bitcoin': 'BTC-XEM', 'lumen-bitcoin': 'BTC-XLM', 'magi-bitcoin': 'BTC-XMG', 'monero-bitcoin': 'BTC-XMR', 'ripple-bitcoin': 'BTC-XRP', 'stealthcoin-bitcoin': 'BTC-XST', 'vcash-bitcoin': 'BTC-XVC', 'verge-bitcoin': 'BTC-XVG', 'whitecoin-bitcoin': 'BTC-XWC', 'zcoin-bitcoin': 'BTC-XZC', 'zclassic-bitcoin': 'BTC-ZCL', 'zcash-bitcoin': 'BTC-ZEC', 'zencash-bitcoin': 'BTC-ZEN', 'firstblood-ethereum': 'ETH-1ST', 'adtoken-ethereum': 'ETH-ADT', 'adex-ethereum': 'ETH-ADX', 'aragon-ethereum': 'ETH-ANT', 'basic attention token-ethereum': 'ETH-BAT', 'bancor-ethereum': 'ETH-BNT', 'cofound.it-ethereum': 'ETH-CFI', 'creditbit-ethereum': 'ETH-CRB', 'dash-ethereum': 'ETH-DASH', 'digix dao-ethereum': 'ETH-DGD', 'ethereum classic-ethereum': 'ETH-ETC', 'funfair-ethereum': 'ETH-FUN', 'gnosis-ethereum': 'ETH-GNO', 'golem-ethereum': 'ETH-GNT', 'guppy-ethereum': 'ETH-GUP', 'humaniq-ethereum': 'ETH-HMQ', 'legends-ethereum': 'ETH-LGD', 'litecoin-ethereum': 'ETH-LTC', 'lunyr-ethereum': 'ETH-LUN', 'monaco-ethereum': 'ETH-MCO', 'metal-ethereum': 'ETH-MTL', 'mysterium-ethereum': 'ETH-MYST', 'numeraire-ethereum': 'ETH-NMR', 'tenx pay token-ethereum': 'ETH-PAY', 'patientory-ethereum': 'ETH-PTOY', 'quantum resistant ledger-ethereum': 'ETH-QRL', 'augur-ethereum': 'ETH-REP', 'iex.ec-ethereum': 'ETH-RLC', 'siacoin-ethereum': 'ETH-SC', 'singulardtv-ethereum': 'ETH-SNGLS', 'status network token-ethereum': 'ETH-SNT', 'storj-ethereum': 'ETH-STORJ', 'chronobank time-ethereum': 'ETH-TIME', 'tokencard-ethereum': 'ETH-TKN', 'trustcoin-ethereum': 'ETH-TRST', 'wings dao-ethereum': 'ETH-WINGS', 'ripple-ethereum': 'ETH-XRP', 'zcash-ethereum': 'ETH-ZEC', 'bitcoin-tether': 'USDT-BTC', 'ethereum classic-tether': 'USDT-ETC', 'ethereum-tether': 'USDT-ETH', 'litecoin-tether': 'USDT-LTC', 'ripple-tether': 'USDT-XRP', 'zcash-tether': 'USDT-ZEC', 'omisego-bitcoin': 'BTC-OMG', 'omisego-ethereum': 'ETH-OMG', 'civic-bitcoin': 'BTC-CVC', 'civic-ethereum': 'ETH-CVC', 'particl-bitcoin': 'BTC-PART', 'qtum-bitcoin': 'BTC-QTUM', 'qtum-ethereum': 'ETH-QTUM'}
xbtcePairs = {'dash-bitcoin': 'DSHBTC', 'emercoin-bitcoin': 'EMCBTC', 'ethereum-bitcoin': 'ETHBTC', 'litecoin-ethereum': 'ETHLTC', 'litecoin-bitcoin': 'LTCBTC', 'namecoin-bitcoin': 'NMCBTC', 'peercoin-bitcoin': 'PPCBTC'}
hitbtcPairs = {'bytecoin-bitcoin': 'BCNBTC', 'dash-bitcoin': 'DASHBTC', 'dogecoin-bitcoin': 'DOGEBTC', 'emercoin-bitcoin': 'EMCBTC', 'ethereum-bitcoin': 'ETHBTC', 'lisk-bitcoin': 'LSKBTC', 'litecoin-bitcoin': 'LTCBTC', 'nxt-bitcoin': 'NXTBTC', 'steem-bitcoin': 'STEEMBTC', 'nem-bitcoin': 'XEMBTC', 'monero-bitcoin': 'XMRBTC', 'ardor-bitcoin': 'ARDRBTC', 'zcash-bitcoin': 'ZECBTC', 'waves-bitcoin': 'WAVESBTC', 'iconomi-bitcoin': 'ICNBTC', 'gnosis-bitcoin': 'GNOBTC', 'monero-ethereum': 'XMRETH', 'ethereum classic-ethereum': 'ETCETH', 'dash-ethereum': 'DASHETH', 'zcash-ethereum': 'ZECETH', 'gnosis-ethereum': 'GNOETH', 'ripple-bitcoin': 'XRPBTC', 'strats-bitcoin': 'STRATBTC'}

usePairs = [bitfinexPairs, krakenPairs, poloniexPairs, xbtcePairs, hitbtcPairs]
totalPairs = [hitbtcPairs, bitfinexPairs, krakenPairs, poloniexPairs, cryptopiaPairs, bittrexPairs, xbtcePairs]

#This function pulls information from all exchanges based on a given coin pair
def aggregateOrders(coinPair):
    asks, bids, exchanges = [], [], []
    try:
        pAsk, pBid = poloniex.topAskBid(poloniexPairs[coinPair])
        asks.append(pAsk)
        bids.append(pBid)
        exchanges.append('poloniex')
        print("Success: Poloniex - Ask:", pAsk, "Bid:",pBid)
    except:
        print("Failure: Poloniex")
        
    try:
        kAsk, kBid = kraken.topAskBid(krakenPairs[coinPair])
        asks.append(kAsk)
        bids.append(kBid)
        exchanges.append('kraken')
        print("Success: Kraken - Ask:", kAsk, "Bid:",kBid)
    except:
        print("Failure: Kraken")
        
    try:
        cAsk, cBid = cryptopia.topAskBid(cryptopiaPairs[coinPair])
        asks.append(cAsk)
        bids.append(cBid)
        exchanges.append('cryptopia')
        print("Success: Cryptopia - Ask:", cAsk, "Bid:", cBid)
    except:
        print("Failure: Cryptopia")
        
    try:
        bAsk, bBid = bitfinex.topAskBid(bitfinexPairs[coinPair])
        asks.append(bAsk)
        bids.append(bBid)
        exchanges.append('bitfinex')
        print("Success: Bitfinex - Ask:", bAsk, "Bid:", bBid)
    except:
        print("Failure: Bitfinex")
        
    try:
        bAsk, bBid = bittrex.topAskBid(bittrexPairs[coinPair])
        asks.append(bAsk)
        bids.append(bBid)
        exchanges.append('bittrex')
        print("Success: Bittrex - Ask:", bAsk, "Bid:", bBid)
    except:
        print("Failure: Bittrex")
        
    try:
        bAsk, bBid = xbtce.topAskBid(xbtcePairs[coinPair])
        asks.append(bAsk)
        bids.append(bBid)
        exchanges.append('xbtce')
        print("Success: xBTCe - Ask:", bAsk, "Bid:", bBid)
    except:
        print("Failure: xBTCe")
    
    try:
        bAsk, bBid = hitbtc.topAskBid(hitbtcPairs[coinPair])
        asks.append(bAsk)
        bids.append(bBid)
        exchanges.append('hitbtc')
        print("Success: HitBTC - Ask:", bAsk, "Bid:", bBid)
    except:
        print("Failure: HitBTC")

    return asks, bids, exchanges
        
#This function checks to see if there's a discrepency
def checkForDifference(coin, percentThreshold = 0.5):
    asks, bids, exchanges = aggregateOrders(coin)
    try:
        #Get difference information
        avg = np.mean(asks+bids)
        maximum = max(bids)
        minimum = min(asks)
        diff = maximum-minimum
        pct = (diff/avg)*100

        #if the percentages is above the threshold, then report it
        if pct >= percentThreshold:
            print('Discrepency')
            cheap = exchanges[asks.index(minimum)]
            expensive = exchanges[bids.index(maximum)]
            return (coin, diff, pct, avg, cheap, expensive)
        #otherwise, just ignore
        else:
            print('No Discrepency')
    except:
        print('Error')

#writes a log of current state as the timestamp
def writeLog(log):
    toWrite = pd.DataFrame(log)
    toWrite.columns = ['Coin Pair', 'Price Difference', 'Percent Difference', 'Price Average', 'Cheap Exchange', 'Expensive Exchange']
    path = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    toWrite.to_csv('logs/'+path+'.csv')
    return []

#continually checks for winning numbers
def makeMoney(listOfPairs, numWins=50):
    winners = []
    while True:
        if len(winners) >= numWins:
            winners = writeLog(winners)
            print('\nLog Written\n')
            
        for group in listOfPairs:
            for token in group.keys():
                winner = checkForDifference(token)
                if winner:
                    winners.append(winner)
                    if winner[2] > 1:
                        body = winner[0]+' has discrepency of '+str(winner[1])+' which is '+str(winner[2]*100)+' percent'
                        message = cli.messages.create(body=body, from_=myTwilioNumber, to=myCellPhone)
                        print('\n-----MESSAGE SENT-----\n')
                time.sleep(15)
    return winners
