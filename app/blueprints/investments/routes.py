from flask import render_template, jsonify, request
from app.blueprints.investments import investments_bp

INVESTMENT_INSTRUMENTS = [
    {
        "id": "stocks",
        "name": "Stocks (Direct Equity)",
        "category": "Equity",
        "risk_level": "Very High",
        "risk_badge": "danger",
        "horizon": "5+ Years",
        "liquidity": "High (T+1 Settlement)",
        "min_investment": "Cost of 1 share (~₹10 to ₹5,000+)",
        "definition": "Shares representing fractional ownership in a publicly traded corporation listed on NSE/BSE.",
        "how_it_works": "You buy shares of companies via a SEBI-registered broker and Demat account. Wealth is created through share price appreciation and quarterly/annual cash dividends.",
        "tax_considerations": "STCG (held ≤ 1 year): Taxed at 20% + surcharge. LTCG (held > 1 year): Taxed at 12.5% on gains exceeding ₹1.25 lakh/year.",
        "advantages": [
            "Highest long-term wealth creation potential among liquid asset classes.",
            "Ownership rights, voting privileges, and regular dividend income.",
            "Extreme liquidity via electronic NSE/BSE exchanges."
        ],
        "disadvantages": [
            "Severe short-term volatility; risk of total capital loss on poorly chosen companies.",
            "Requires extensive financial analysis, balance sheet reading, and emotional control."
        ],
        "important_risks": "Market risk, business bankruptcy risk, regulatory changes, and lack of diversification if concentrated.",
        "calculator": "sip"
    },
    {
        "id": "mutual_funds",
        "name": "Mutual Funds",
        "category": "Equity / Debt / Hybrid",
        "risk_level": "Moderate to High",
        "risk_badge": "warning",
        "horizon": "3 to 10+ Years",
        "liquidity": "High (1-3 business days)",
        "min_investment": "₹500 (Lump sum or SIP)",
        "definition": "A professionally managed investment pool that collects funds from thousands of investors to buy a basket of securities.",
        "how_it_works": "Asset Management Companies (AMCs) deploy pooled funds according to scheme objectives. Full-time professional fund managers research and rebalance the portfolio.",
        "tax_considerations": "Equity funds: 20% STCG / 12.5% LTCG above ₹1.25L. Debt funds: Taxed at your individual slab rate. ELSS funds offer up to ₹1.5L deduction under Sec 80C.",
        "advantages": [
            "Instant portfolio diversification with as little as ₹500.",
            "Professional management overseen by stringent SEBI regulations.",
            "Easy automation through monthly bank auto-debit (SIP)."
        ],
        "disadvantages": [
            "Subject to market risks; returns are never guaranteed.",
            "Annual expense ratio fee charged by the fund house."
        ],
        "important_risks": "Underlying market movements, portfolio manager underperformance, and fund manager style drift.",
        "calculator": "sip"
    },
    {
        "id": "sip",
        "name": "SIP (Systematic Investment Plan)",
        "category": "Investment Method",
        "risk_level": "Depends on underlying fund",
        "risk_badge": "info",
        "horizon": "5 to 20+ Years",
        "liquidity": "High (Open-ended funds)",
        "min_investment": "₹100 to ₹500 / month",
        "definition": "A disciplined method of investing a fixed rupee amount regularly into mutual funds rather than a one-time lump sum.",
        "how_it_works": "On your designated date each month, your bank auto-debits ₹X and purchases units at that day's NAV, practicing Rupee Cost Averaging.",
        "tax_considerations": "Each individual monthly SIP installment is treated as an independent investment for holding period calculation (FIFO method).",
        "advantages": [
            "Averages out purchase price: buys more units during market dips.",
            "Instills saving discipline and removes emotional timing errors.",
            "Can be started, paused, increased, or stopped anytime online."
        ],
        "disadvantages": [
            "Does not eliminate market risk; returns depend entirely on underlying fund performance."
        ],
        "important_risks": "Prolonged economic stagnation leading to lower-than-expected compound returns.",
        "calculator": "sip"
    },
    {
        "id": "equity_funds",
        "name": "Equity Mutual Funds (Large/Mid/Small)",
        "category": "Equity",
        "risk_level": "High to Very High",
        "risk_badge": "danger",
        "horizon": "5+ Years",
        "liquidity": "High (T+2 days)",
        "min_investment": "₹500 / month",
        "definition": "Mutual funds that invest at least 65% of their total assets in equity shares of domestic companies.",
        "how_it_works": "Classified by market cap: Large-Cap (top 100 blue chips), Mid-Cap (101-250), Small-Cap (251+), and Multi-Cap/Flexi-Cap (across all caps).",
        "tax_considerations": "LTCG above ₹1.25 lakh taxed at 12.5%. STCG taxed at 20%.",
        "advantages": [
            "Consistently beats consumer price inflation over multi-decade cycles.",
            "Wide variety tailored to individual risk tolerance levels."
        ],
        "disadvantages": [
            "Small and mid-cap funds can drop 30-50% in bear market corrections."
        ],
        "important_risks": "High drawdown risk in small caps; sector concentration risk in thematic funds.",
        "calculator": "sip"
    },
    {
        "id": "debt_funds",
        "name": "Debt Mutual Funds",
        "category": "Debt",
        "risk_level": "Low to Moderate",
        "risk_badge": "primary",
        "horizon": "1 Day to 3 Years",
        "liquidity": "Very High (T+1 days)",
        "min_investment": "₹500",
        "definition": "Funds that invest in fixed-income securities like Treasury bills, Government bonds, Commercial Paper (CP), and Certificates of Deposit (CD).",
        "how_it_works": "The fund earns interest from debt instruments and capital gains when market interest rates fall, distributing returns via daily NAV appreciation.",
        "tax_considerations": "Gains are taxed at individual income tax slab rates regardless of holding period (post-Finance Act 2023 amendment).",
        "advantages": [
            "Far higher stability and lower price fluctuations than equity funds.",
            "Liquid and Overnight funds provide better utility than idle savings accounts."
        ],
        "disadvantages": [
            "Lower return potential than equities; yields usually match inflation/FD rates.",
            "Loss of indexation tax benefits since April 2023."
        ],
        "important_risks": "Credit/default risk if corporate issuers fail, and interest rate duration risk.",
        "calculator": "compound"
    },
    {
        "id": "index_funds",
        "name": "Index Funds",
        "category": "Passive Equity",
        "risk_level": "Moderate to High",
        "risk_badge": "warning",
        "horizon": "5+ Years",
        "liquidity": "High (T+2 days)",
        "min_investment": "₹100 to ₹500",
        "definition": "Passive mutual funds designed to mirror the composition and performance of a market benchmark like Nifty 50 or BSE Sensex.",
        "how_it_works": "Holds the exact 50 or 30 stocks in identical index weights. No fund manager picks or drops stocks subjectively.",
        "tax_considerations": "Treated as equity funds: 12.5% LTCG above ₹1.25L; 20% STCG.",
        "advantages": [
            "Rock-bottom expense ratios (often 0.10%–0.25% vs 1.5% for active funds).",
            "Eliminates human manager bias and underperformance risk.",
            "Historical data shows index funds beat 70%+ active large-cap funds over 10 years."
        ],
        "disadvantages": [
            "Cannot outperform the benchmark; drops in lockstep when the market falls."
        ],
        "important_risks": "Overall macroeconomic market contractions and tracking error.",
        "calculator": "sip"
    },
    {
        "id": "etfs",
        "name": "ETFs (Exchange Traded Funds)",
        "category": "Passive Equity / Gold / Debt",
        "risk_level": "Moderate to High",
        "risk_badge": "warning",
        "horizon": "3+ Years",
        "liquidity": "High (Traded on exchange)",
        "min_investment": "Cost of 1 unit (~₹20 to ₹300)",
        "definition": "Marketable securities that track an index, commodity, or bonds, traded live on stock exchanges like individual shares.",
        "how_it_works": "Bought and sold during exchange trading hours (9:15 AM - 3:30 PM) via Demat account at real-time market prices, unlike mutual funds priced at end-of-day NAV.",
        "tax_considerations": "Equity ETFs taxed as equity (20% STCG / 12.5% LTCG). Gold & Debt ETFs taxed at slab rates.",
        "advantages": [
            "Real-time intraday pricing and flexibility to place limit/stop-loss orders.",
            "Ultra-low internal expense ratios."
        ],
        "disadvantages": [
            "Requires an active Demat and trading account; broker brokerage fees apply.",
            "Liquidity volume can be low in niche ETFs, creating bid-ask spread costs."
        ],
        "important_risks": "Liquidity risk on exchange and tracking difference from index.",
        "calculator": "compound"
    },
    {
        "id": "bonds",
        "name": "Corporate Bonds & Debentures",
        "category": "Debt",
        "risk_level": "Moderate",
        "risk_badge": "primary",
        "horizon": "1 to 10 Years",
        "liquidity": "Moderate (Secondary market)",
        "min_investment": "₹1,000 to ₹10,000 via modern bond platforms",
        "definition": "Debt securities issued by private or public corporations to raise capital from retail and institutional investors.",
        "how_it_works": "You lend money to the corporation in exchange for regular coupon (interest) payments and return of principal at maturity. Rated by agencies like CRISIL/ICRA (AAA down to D).",
        "tax_considerations": "Coupon interest is added to your income and taxed at slab rates. Capital gains taxed at slab rates.",
        "advantages": [
            "Predictable cash flows through scheduled semi-annual or annual interest.",
            "AAA and AA+ bonds typically offer 1-2% higher yields than bank FDs."
        ],
        "disadvantages": [
            "Lower liquidity than mutual funds; secondary market selling may take time.",
            "Default risk if company financial health deteriorates."
        ],
        "important_risks": "Credit rating downgrades and borrower default risk.",
        "calculator": "compound"
    },
    {
        "id": "gsecs",
        "name": "Government Securities (G-Secs)",
        "category": "Sovereign Debt",
        "risk_level": "Zero Credit Risk",
        "risk_badge": "success",
        "horizon": "1 to 40 Years",
        "liquidity": "Moderate (RBI Retail Direct)",
        "min_investment": "₹10,000 via RBI Retail Direct",
        "definition": "Tradable debt instruments issued by the Central Government or State Governments acknowledging the government's debt obligation.",
        "how_it_works": "Accessible directly to individual retail citizens through RBI's Retail Direct Portal with zero intermediary commission.",
        "tax_considerations": "Interest income is fully taxable according to your income tax slab.",
        "advantages": [
            "Sovereign guarantee: Absolutely zero risk of credit default.",
            "Wide variety of maturities available, from 1-year bonds to 40-year bonds."
        ],
        "disadvantages": [
            "Interest is fully taxable at slab rate, reducing net yield for 30% slab earners.",
            "Bond prices fall when RBI raises market interest rates."
        ],
        "important_risks": "Interest rate risk (market price fluctuations before maturity).",
        "calculator": "compound"
    },
    {
        "id": "tbills",
        "name": "Treasury Bills (T-Bills)",
        "category": "Money Market",
        "risk_level": "Zero Credit Risk",
        "risk_badge": "success",
        "horizon": "91, 182, or 364 Days",
        "liquidity": "High",
        "min_investment": "₹10,000",
        "definition": "Short-term sovereign debt instruments issued by the Government of India for maturities up to 1 year.",
        "how_it_works": "Zero-coupon securities: issued at a discount to face value and redeemed at full face value (₹100) upon maturity. The difference represents the investor's return.",
        "tax_considerations": "The discount gained at maturity is treated as Short-Term Capital Gains and taxed at slab rates.",
        "advantages": [
            "100% sovereign safety with short tenure commitment.",
            "Ideal avenue for parking surplus business or personal cash safely."
        ],
        "disadvantages": [
            "Yields are linked to short-term money market rates and don't provide long-term capital compounding."
        ],
        "important_risks": "Re-investment risk upon maturity.",
        "calculator": "compound"
    },
    {
        "id": "ppf",
        "name": "PPF (Public Provident Fund)",
        "category": "Government Scheme",
        "risk_level": "Zero Risk (Sovereign)",
        "risk_badge": "success",
        "horizon": "15 Years (Extendable in 5-yr blocks)",
        "liquidity": "Low (Locked-in; partial loans/withdrawals after 6 yrs)",
        "min_investment": "₹500 / year (Max ₹1,50,000 / year)",
        "definition": "A 15-year statutory savings and tax-saving instrument guaranteed by the Central Government of India.",
        "how_it_works": "Deposits earn interest fixed quarterly by the Ministry of Finance (currently ~7.1% p.a.), compounded annually on March 31st.",
        "tax_considerations": "EEE (Exempt-Exempt-Exempt): Investment qualifies for Sec 80C deduction; Interest is 100% tax-free; Maturity is 100% tax-free.",
        "advantages": [
            "Completely tax-free interest and maturity under Indian income tax law.",
            "Protected by law: PPF balances cannot be attached by court orders or creditors.",
            "Safe long-term compounding bedrock for retirement."
        ],
        "disadvantages": [
            "Strict 15-year lock-in period.",
            "Capped at ₹1.5 lakh maximum deposit per financial year."
        ],
        "important_risks": "Low liquidity and interest rate revisions by the Ministry of Finance.",
        "calculator": "compound"
    },
    {
        "id": "nps",
        "name": "NPS (National Pension System)",
        "category": "Retirement Pension",
        "risk_level": "Moderate (Market-linked)",
        "risk_badge": "warning",
        "horizon": "Until Age 60",
        "liquidity": "Low (Locked until age 60)",
        "min_investment": "₹1,000 / year",
        "definition": "A voluntary government-sponsored defined-contribution pension scheme regulated by PFRDA.",
        "how_it_works": "Contributions are allocated across Equity (E), Corporate Debt (C), and Government Securities (G) by professional pension managers.",
        "tax_considerations": "Deductions up to ₹1.5L under 80CCD(1), PLUS an exclusive additional ₹50,000 under Section 80CCD(1B). At age 60: 60% lump sum is 100% tax-free; 40% buys a taxable monthly pension (annuity).",
        "advantages": [
            "Lowest fund management fee in the world (approx 0.09%).",
            "Exclusive ₹50,000 additional income tax deduction.",
            "Forces disciplined compounding until retirement age."
        ],
        "disadvantages": [
            "Mandatory 40% annuity purchase at age 60; annuity yields are usually modest (5.5-6.5%) and taxable."
        ],
        "important_risks": "Market fluctuations affecting equity portfolio and post-retirement annuity rate risk.",
        "calculator": "sip"
    },
    {
        "id": "fixed_deposits",
        "name": "Bank Fixed Deposits (FDs)",
        "category": "Fixed Income",
        "risk_level": "Very Low (Up to ₹5L DICGC)",
        "risk_badge": "success",
        "horizon": "7 Days to 10 Years",
        "liquidity": "High (Premature withdrawal penalty ~0.5-1%)",
        "min_investment": "₹1,000",
        "definition": "A term deposit with a scheduled bank offering guaranteed interest over a contracted time period.",
        "how_it_works": "You deposit a lump sum. The bank pays agreed interest, typically compounded quarterly, and returns principal + interest at maturity.",
        "tax_considerations": "Interest is fully taxable as income from other sources. 10% TDS if annual interest exceeds ₹40,000 (₹50,000 for seniors). 5-year tax-saving FDs qualify under Sec 80C.",
        "advantages": [
            "Fixed guaranteed returns regardless of stock market fluctuations.",
            "Insured up to ₹5,00,000 per depositor per bank by DICGC.",
            "Senior citizens enjoy an additional 0.25% to 0.75% interest bonus."
        ],
        "disadvantages": [
            "Post-tax returns often fail to beat retail inflation for 30% tax slab individuals.",
            "Premature penalty reduces contracted rate by 0.5%–1%."
        ],
        "important_risks": "Inflation erosion risk (negative real return after tax and inflation).",
        "calculator": "fd"
    },
    {
        "id": "gold",
        "name": "Gold (Sovereign Gold Bonds / Gold ETFs)",
        "category": "Commodity / Hedge",
        "risk_level": "Moderate",
        "risk_badge": "primary",
        "horizon": "5 to 8+ Years",
        "liquidity": "High (ETFs / Secondary SGB)",
        "min_investment": "1 gram (~₹7,000-8,000)",
        "definition": "Investment in gold bullion either digitally via Gold ETFs or through RBI-issued Sovereign Gold Bonds (SGBs).",
        "how_it_works": "SGBs: Issued by RBI on behalf of Government of India with an 8-year tenure. Pays 2.50% annual interest on face value, plus gold price appreciation at maturity.",
        "tax_considerations": "SGBs: 100% Capital gains tax-exempt if held to full 8-year maturity. Gold ETFs: Taxed at 12.5% LTCG if held > 2 years.",
        "advantages": [
            "Classic historical hedge against currency depreciation and global geopolitical turmoil.",
            "SGBs pay 2.5% semi-annual cash interest on top of gold appreciation.",
            "Eliminates storage, locker charges, purity doubts, and making charge losses of physical gold."
        ],
        "disadvantages": [
            "Gold does not generate productive corporate profits or business cash flows.",
            "Long multi-year periods of zero or stagnant price movements can occur."
        ],
        "important_risks": "Global commodity price cycles and currency exchange rate shifts.",
        "calculator": "compound"
    }
]


@investments_bp.route("/")
def index():
    """Investment education dashboard and comparison matrix."""
    return render_template("investments/index.html", instruments=INVESTMENT_INSTRUMENTS)


@investments_bp.route("/api/instruments", methods=["GET"])
def api_instruments():
    """Return JSON list of all investment instruments."""
    category = request.args.get("category")
    risk = request.args.get("risk")
    
    filtered = INVESTMENT_INSTRUMENTS
    if category:
        filtered = [x for x in filtered if x["category"].lower() == category.lower()]
    if risk:
        filtered = [x for x in filtered if risk.lower() in x["risk_level"].lower()]
        
    return jsonify({"success": True, "data": filtered, "count": len(filtered)})
