/**
 * Centralized UI Strings, Form Placeholders, and Internationalization Dictionary
 * Clean architectural separation: zero hardcoded strings inside React components.
 * All user-facing labels, input placeholders, action buttons, and notices reside here.
 */

export const uiStrings = {
  auth: {
    loginTitle: "Sign in to your account",
    loginSubtitle: "Access your enterprise neural visibility dashboard and live competitor benchmarks.",
    signupTitle: "Create your workspace",
    signupSubtitle: "Start tracking citations and AI brand presence across Gemini, ChatGPT, Claude, and Perplexity.",
    labels: {
      fullName: "Full Name",
      companyWebsite: "Company Website",
      workEmail: "Work Email or Username",
      password: "Password",
    },
    placeholders: {
      fullName: "",
      companyWebsite: "https://company.com",
      workEmail: "name@company.com",
      password: "••••••••",
    },
    buttons: {
      signIn: "Sign In",
      signUp: "Create Account",
      submitting: "Processing...",
      continueWithGoogle: "Continue with Google",
      switchModeToSignUp: "Sign Up",
      switchModeToSignIn: "Sign In",
    },
    notices: {
      termsAgreement: "By continuing, you agree to our Terms of Service and Privacy Policy.",
      securityBadge: "Enterprise-grade AES-256 encryption & SOC2 Type II compliance.",
    },
  },

  landing: {
    hero: {
      titlePrefix: "Humans don't visit your website anymore—",
      titleEmphasis: "AI does.",
      subtitle: "EsooAI gets your site AI-ready so you show up in answers, get cited, and grow revenue.",
      inputPlaceholder: "Enter your website URL",
      auditButton: "Run AI visibility audit",
      auditingButton: "Auditing...",
      recentSearches: {
        title: "Recent Searches",
        clearAll: "Clear",
        empty: "No recent searches found",
      },
    },
    auditModal: {
      closeTooltip: "Close and return to search",
      promptsPrefix: "Here are a few prompts",
      promptsSuffix: "may be cited in:",
      estimatedMentionRate: "Estimated Mention Rate",
      signInButton: "Sign In to Access Dashboard",
      createAccountButton: "Create Enterprise Account",
      disclaimer: "Real-time empirical consensus benchmark across frontier LLMs.",
    },
  },

  navigation: {
    product: "Product",
    useCases: "Use cases",
    resources: "Resources",
    pricing: "Pricing",
    signIn: "Sign in",
    getStarted: "Get Started",
  },
} as const;

export type UiStrings = typeof uiStrings;
