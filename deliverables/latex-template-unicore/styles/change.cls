%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% -*- Mode: Latex -*- %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% change.cls ---
%%
%% Filename: change.cls
%% Description:
%% Authors: Mohamed Ahmed <m.ahmed@cs.ucl.ac.uk> @CHANGE / Emil Slusanschi <emil.slusanschi@cs.pub.ro> @UNICORE
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%
%%% Change log:
%% $Date$
%% $Revision$
%% $Id$
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand\@classname {UNICORE doc}
\def \fileversion{v1.0}
\def \filedate{2011/01/22}
\def \docdate{\filedate}
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{change}[\filedate\space\fileversion\space UNICORE doc class]
\DeclareOption{twocolumn}{%
  \ClassError{change_document}{Option `twocolumn' not supported.}{}}
\newif \if@draftmode
\@draftmodefalse
\DeclareOption{draft}{\@draftmodetrue\PassOptionsToClass{draft}{book}}
\DeclareOption{final}{\@draftmodefalse\PassOptionsToClass{final}{book}}
\PassOptionsToClass{a4paper}{book}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions
\LoadClass{book}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Document header and footer  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{fancyhdr, lastpage}
\RequirePackage{styles/change_a4}
\RequirePackage{times}
\RequirePackage{ifthen}

%
% Warn if user does not set the required variables in preamble
\begingroup\lccode`!=`\\\lowercase{\endgroup\def\@backslashchar{!}}
\newcommand\checkpreamble{
  %% check the abstract is set 
  \ifx\@abstract\@empty
     \@latex@warning{\@classname: \@backslashchar abstract not defined in preamble}
     \def\@abstract{Your abstract goes here }
  \else
    \relax
  \fi
  %% check the target audience is set 
  \ifx\@targetAudience\@empty
     \@latex@warning{\@classname: \@backslashchar targetAudience not defined in preamble}
     \def\@targetAudience{Your Target Audience goes here }
  \fi
}

\AtBeginDocument{
  \checkpreamble
}


%%%%%%%%%%%%%%%%%%%
% Page dimensions %
%%%%%%%%%%%%%%%%%%%
\setlength \topmargin {10\p@}   %% margin from the top
% \setlength \textwidth {450\p@}  %% the width of the text
% \setlength \textheight {705\p@} %% the height of the text
\setlength \textwidth {475\p@}  %% the width of the text
\setlength \textheight {725\p@} %% the height of the text

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% page dependant margin set up - we can fix later -mahmed  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% \setlength \oddsidemargin {96\p@}
%% \if@twoside
%%   \setlength \evensidemargin {60\p@}
%% \else
%%   \setlength \evensidemargin {96\p@}
%% \fi
\setlength \oddsidemargin {60\p@}
\setlength \evensidemargin {60\p@}

\setlength \parindent{0em}             %
\setlength \parskip  {\z@ \@plus 0.5\p@} %
\setlength \headsep  {30\p@}           %
\ifcase \@ptsize                       %
  \setlength \footskip{26\p@}          %
\or                                    %
  \setlength \footskip{27\p@}          %
\or                                    %
  \setlength \footskip{28\p@}          %
\fi                                    %



%%
\setlength \partopsep {\z@}
\tolerance = \@m
\emergencystretch = 10\p@
\vfuzz = 2\p@
\hfuzz = 2\p@
\flushbottom

\renewcommand \baselinestretch{1.5}

%%%%%%%%%%%%%%%%%%%%%%%%%%
% the table of contents  %
%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand \tableofcontents{%
  %\setlength \headsep  {30\p@}
  \if@twocolumn%
     \@restonecoltrue \onecolumn%
  \else%
     \@restonecolfalse%
  \fi%
  \chapter*{%
    \contentsname%
    \@mkboth{\contentsname}{\contentsname}%
  }%
  \@starttoc{toc}%
  \if@restonecol%
    \twocolumn%
  \fi%
}

%%%%%%%%%%%%%%%%%%%%%%%
% the list of figures %
%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand \listoffigures{%
    \if@twocolumn%
        \@restonecoltrue \onecolumn%
    \else%
        \@restonecolfalse%
    \fi%
    \chapter*{%
        \listfigurename%
        \@mkboth{\listfigurename}{\listfigurename}%
        \addcontentsline{toc}{chapter}{ \listfigurename}
    }%
    \@starttoc{lof}%
    \if@restonecol%
    \twocolumn%
    \fi%
}

%%%%%%%%%%%%%%%%%%%%%%%
% the list of tables  %
%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand \listoftables{%
    \if@twocolumn%
        \@restonecoltrue \onecolumn%
    \else%
        \@restonecolfalse%
    \fi%
    \chapter*{%
        \listtablename%
        \@mkboth{\listtablename}{\listtablename}%
        \addcontentsline{toc}{chapter}{\listtablename}
    }%
    \@starttoc{lot}%
    \if@restonecol%
        \twocolumn%
    \fi%
}

%%%%%%%%%%%%%%%%%%%%%
% the bibliography  %
%%%%%%%%%%%%%%%%%%%%%
\renewenvironment{thebibliography}[1]{%
    \chapter*{%
        \bibname%
        \@mkboth{\bibname}{\bibname}%
    }%
    \list{\@biblabel{\arabic{enumiv}}}%
         {\settowidth \labelwidth{\@biblabel{#1}}%
          \leftmargin \labelwidth%
          \advance \leftmargin \labelsep%
          \@openbib@code%
          \usecounter{enumiv}%
          \let \p@enumiv \@empty%
          \renewcommand \theenumiv{\arabic{enumiv}}%
         }%
    \sloppy%
    \clubpenalty 4000%
    \@clubpenalty \clubpenalty%
    \widowpenalty 4000%
    \sfcode`\.=\@m%
}{%
    \def \@noitemerr{\@latex@warning{Empty `thebibliography' environment}}%
    \endlist%
}


%%%%%%%%%%%%%%%%%%%%%%%
% the document index  %
%%%%%%%%%%%%%%%%%%%%%%%
\renewenvironment{theindex}{%
    \if@twocolumn%
        \@restonecolfalse%
    \else%
        \@restonecoltrue%
    \fi%
    \columnseprule \z@%
    \columnsep 35\p@%
    \twocolumn[\@makeschapterhead{\indexname}]%
    \@mkboth{\indexname}{\indexname}%
    \thispagestyle{plain}%
    \small%
    \parindent \z@%
    \parskip \z@ \@plus .3\p@%
    \relax%
%%%
%%%  It appears that there is an error in the definition of \@idxitem
%%%  which causes horrid looking indexes.  Redefine the miscreant
%%%  so as to insert the missing \par.  NB.  Cannot use
%%%  |\renewcommand| since this appears not to work on outer block,
%%%  even if |\global| is used.
%%%
%%%  As noticed on 1998.03.15, this appears to have been fixed.
%%%
%%%    \gdef \@idxitem{\par \hangindent 40\p@}
%%%
    \let \item \@idxitem%
}{%
    \if@restonecol%
        \onecolumn%
    \else%
       % \clearpage%
    \fi%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% the document title page  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand \makeTitlePage{%
    \thispagestyle{changeFrontPage}%
    \@makeTitlePage%    
    % \let \thanks = \relax%
    % \gdef \@address{}%
    % \gdef \@thanks{}%
    % \gdef \@author{}%
    %\gdef \@title{}%
}

\newcommand \@makeTitlePage{%
  % \newpage%
  \null
  \setcounter{page}{1}%
  \setcounter{footnote}{1}%
  \vfill
  \begin{center}
    %%
    { \large \consortiumICT \\ }
    %%
    { \Large \bfseries \consortiumName \\}
    %%
    \vspace*{0.5cm}
    {\huge \bfseries \@title \\}
    %%
    \vspace*{1.0cm}
    % {\Large \@frmwrkBlurb \\}
    %%
    % \vspace*{2.0cm}%
    % {\huge  \bfseries \@documentTitle \\}
    %%
    {
      \vspace*{2.0cm}%
      % \@documentDueDate \\
      \@documentSubmitDate \\
      \@delivLeadContractor \\
      \@delivVersion \\
    }
  \end{center}%
  
  %% 

  \vfill%
  %% This is the front page lower section
  % \begin{tabular} {p{7.25cm} p{7.8cm}}
  %   \projStartDateK       & {\raggedright \@projStartDate }\\
  %   \projDurationK        & {\raggedright \@projDuration } \\
  %   \delivLeadContractorK & {\raggedright \@delivLeadContractor} \\
  %   \delivVersionK        & {\raggedright \@delivVersion }\\
  %   \delivConfStatusK     & {\raggedright \@delivConfStatus }\\
  % \end{tabular}
  %\vfill%
  \clearpage%
}

\newcommand \makeAbstractPage [1]{%
    \thispagestyle{fancy}
    \@makeAbstractPage {#1}
    %\setcounter{footnote}{0}%
}

\newcommand \@makeAbstractPage[1]{%
  %%
  \null
  { 
    \mkAbstractAndTarget
    \vspace*{1.0cm}%
  }
  
  {   
    \ifthenelse{\equal{#1}{public}} {\@docPublic} { }
      \ifthenelse{\equal{#1}{confidential}} {\@docConfidential} { }     
  }  
  
  {   
    \vfill%  
    \documentImpressum
  }

}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% document environment variables  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\abstract}[1]{\def\@abstract{#1}}
\newcommand{\targetAudience}[1]{\def\@targetAudience{#1}}

\newcommand{\impressum}[1]{\def\@impressum{#1}}
\newcommand{\documentTitle}[1] {\def\@documentTitle{#1}}
\newcommand{\frmwrkBlurb}[1]  {\def\@frmwrkBlurb{#1}}
% \newcommand{\documentDueDate}[1]  {\def\@documentDueDate{Due date of deliverable: #1}}
\newcommand{\documentSubmitDate}[1] {\def\@documentSubmitDate{Date of deliverable: #1}}

\newcommand{\projStartDateK} {Start date of project}
\newcommand{\projStartDate}[1] {\def\@projStartDate{#1}}

\newcommand{\projDurationK} {Duration}
\newcommand{\projDuration}[1] {\def\@projDuration{#1}}

\newcommand{\delivLeadContractorK}{Lead contractor for this deliverable}
\newcommand{\delivLeadContractor}[1] {\def\@delivLeadContractor{Author: #1}}

\newcommand{\delivVersionK}{Version}
\newcommand{\delivVersion}[1] {\def\@delivVersion{Version: #1}}

\newcommand{\delivConfStatusK}{Confidentiality status}
\newcommand{\delivConfStatus}[1] {\def\@delivConfStatus{#1}}

\newcommand{\docPublic}[1] {\def\@docPublic{#1}}
\newcommand{\docConfidential}[1] {\def\@docConfidential{#1}}


% Empty initialisation
\abstract{}
\targetAudience{}
\docConfidential{}
\docPublic{}
\impressum{}
\frmwrkBlurb{}
%\documentDueDate{}

 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % the abstract and target audience section  %
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{mkAbstractAndTarget}{% 
  \begin{tabular}{|p{0.95\textwidth}|}
    \hline
    {\centering  \large \textbf{Abstract} \\  }
    \@abstract \\
    {\centering \large \textbf{Target Audience} \\  }  
    \@targetAudience \\
    \hline
  \end{tabular}    
}
{\footnotesize %
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% the document legalities section  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{mkDocLegal}{% 
  \begin{tabular}{|p{0.95\textwidth}|}
    \hline
    {\centering  \large \textbf{Abstract} \\  }
    \@abstract \\
    {\centering \large \textbf{Target Audience} \\  }  
    \@targetAudience \\
    \hline
  \end{tabular}    
}
{\footnotesize %
}



%%%%%%%%%%%%%%%%%%%%%%
% document keywords  %
%%%%%%%%%%%%%%%%%%%%%%
\newcommand \@keywords{\textbf{Keywords}}
\newenvironment{keywords}{%
  {\large \noindent \@keywords :} \\%
  \@mkboth{\@keywords}{\@keywords}%
}{\footnotesize %
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% document acknowledgements  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand \@acknowledgements{Acknowledgements}
\newenvironment{acknowledgements}{%
    \chapter*{\@acknowledgements}%
    \@mkboth{\@acknowledgements}{\@acknowledgements}%
}


%%%%%%%%%%%%%%%%%%%%%
% chapter headings  %
%%%%%%%%%%%%%%%%%%%%%
\renewcommand\chapter{%
  \clearpage%
  \thispagestyle{fancy}%
  \global \@topnum \z@%
  \@afterindentfalse%
  \secdef \@chapter \@schapter%
}

% numbered chapter heading style:
\renewcommand{\@makechapterhead}[1]{%
  {\parindent \z@%
    \raggedright%
    \reset@font%
    \ifnum \c@secnumdepth >\m@ne%
      \if@mainmatter%
        \huge \bfseries  \thechapter \hspace{1.5cm} %
      \fi%
    \fi%
    \huge \bfseries #1%
    \par%
    \nobreak%
    \vskip 10\p@%
  }
  %% \addcontentsline{toc}{part}{#1}
}

% Unnumbered chapter heading style:
\renewcommand{\@makeschapterhead}[1]{%
  {\parindent \z@%
    \raggedright%
    \reset@font%
    \huge \bfseries #1%
    \par%
    \nobreak%
    \vskip 10\p@%
  }
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% section/section* definition %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand*{\section}{\@ifstar\@sectionstar\@section}%
\newcommand\@section[2][]{%
  \makeatletter
  \renewcommand{\@seccntformat}[1]
  {\textbf{\csname the##1\endcsname} \hspace{1.2cm}}
  \makeatother
  \@startsection {section}{1}{\z@}%
                 {-1ex \@plus -.4ex \@minus -.2ex}%
                 {.6ex \@plus .1ex}%
                 {\reset@font \Large \bfseries}%
                 {#2}}
\newcommand\@sectionstar[2][]{%
  \@startsection{section}{1}{\z@}%
                 {-1ex \@plus -.4ex \@minus -.2ex}%
                 {.6ex \@plus .1ex}%
                 {\reset@font \Large \bfseries}*{#2}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subsection/subsection* definition %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand*{\subsection}{\@ifstar\@subsectionstar\@subsection}%
\newcommand\@subsection[2][]{%
  \makeatletter
  \renewcommand{\@seccntformat}[1]
  {\textbf{\csname the##1\endcsname} \hspace{1.02cm}}
  \makeatother
  \@startsection {subsection}{2}{\z@}%
                 {-.7ex\@plus -.3ex \@minus -.2ex}%
                 {.4ex \@plus .1ex}%
                 {\reset@font \large \bfseries}{#2}}
\newcommand\@subsectionstar[2][]{%
  \@startsection{subsection}{2}{\z@}%
                {-.7ex\@plus -.3ex \@minus -.2ex}%
                 {.4ex \@plus .1ex}%
                 {\reset@font \large \bfseries}*{#2}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subsubsection/subsubsection* definition %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand*{\subsubsection}{\@ifstar\@subsubsectionstar\@subsubsection}%
\newcommand\@subsubsection[2][]{%
  \makeatletter
  \renewcommand{\@seccntformat}[1]
  {\textbf{\csname the##1\endcsname} \hspace{0.7cm}}
  \makeatother
  \@startsection {subsubsection}{2}{\z@}%
                 {-.5ex\@plus -.2ex \@minus -.2ex}%
                 {.3ex \@plus .1ex}%
                 {\reset@font \large \bfseries}{#2}}
\newcommand\@subsubsectionstar[2][]{%
  \@startsection{subsubsection}{2}{\z@}%
                 {-.5ex\@plus -.2ex \@minus -.2ex}%
                 {.3ex \@plus .1ex}%
                 {\reset@font \large \bfseries}*{#2}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% paragraph/paragraph* definition %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand*{\paragraph}{\@ifstar\@paragraphstar\@paragraph}%
\newcommand\@paragraph[2][]{%
  \makeatletter
  \renewcommand{\@seccntformat}[1]
  {\textbf{\csname the##1\endcsname} \hspace{0.4cm}}
  \makeatother
  \@startsection {paragraph}{2}{\z@}%
                 {-.5ex\@plus -.2ex \@minus -.2ex}%
                 {-.2em \@plus .1ex}%
                 {\reset@font \large \bfseries}{#2}}
\newcommand\@paragraphstar[2][]{%
  \@startsection{paragraph}{2}{\z@}%
                 {-.5ex\@plus -.2ex \@minus -.2ex}%
                 {-.2em \@plus .1ex}%
                 {\reset@font \large \bfseries}*{#2}}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% subparagraph/subparagraph* definition  %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\renewcommand*{\subparagraph}{\@ifstar\@subparagraphstar\@subparagraph}%
\newcommand\@subparagraph[2][]{%
  \makeatletter
  \renewcommand{\@seccntformat}[1]
  {\textbf{\csname the##1\endcsname} \hspace{0.1cm}}
  \makeatother
  \@startsection {subparagraph}{2}{\z@}%
                 {-.5ex\@plus -.2ex \@minus -.2ex}%
                 {-.2em \@plus .1ex}%
                 {\reset@font \large \bfseries}{#2}}
\newcommand\@subparagraphstar[2][]{%
  \@startsection{subparagraph}{2}{\z@}%
                 {-.5ex\@plus -.2ex \@minus -.2ex}%
                 {-.2em \@plus .1ex}%
                 {\reset@font \large \bfseries}*{#2}}


\setcounter{secnumdepth}{5} % the number of subsections to be displayed
\setcounter{tocdepth}{3} % the number of subsections to be displayed
                         % in contents page


% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % NOTE: mahmed use the paragraph environment instead                      %
% %                                                                         %
% % % \newcounter{subsubsubsection}[subsubsection]                          %
% % % \newcommand\subsubsubsection{\@startsection{subsubsubsection}{4}{\z@} %
% % %   {-3.25ex\@plus -1ex \@minus -.2ex}                                  %
% % %   {1.5ex \@plus .2ex}                                                 %
% % %   {\normalfont\normalsize\bfseries}}                                  %
% % % \newcommand*\l@subsubsubsection{\@dottedtocline{3}{10.0em}{4.1em}}    %
% % % \newcommand*{\subsubsubsectionmark}[1]{}                              %
% %                                                                         %
% % % \renewcommand\thesubsubsubsection{                                    %
% % %   \thesubsubsection.\@alph\c@subsubsubsection}                        %
% %                                                                         %
% %                                                                         %
% % % \renewcommand \subsubsubsection{                                      %
% % %   \makeatletter                                                       %
% % %   \renewcommand{\@seccntformat}[1]                                    %
% % %   {\textbf{\csname the##1\endcsname} \hspace{.7cm}}                   %
% % %   \makeatother                                                        %
% % %   \@startsection{subsubsubsection}{3}{\z@}                            %
% % %   {-.5ex\@plus -.2ex \@minus -.2ex}                                   %
% % %   {.3ex \@plus .1ex}                                                  %
% % %   {\reset@font \large \bfseries}                                      %
% % % }                                                                     %
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%
% copyright %
%%%%%%%%%%%%%
\newcommand{\makecopyright}{%
  \hbox{\hfil}\vspace{4in}\begin{center}
  Copyright \copyright\ \the\year\ by \@author \\
  All rights reserved.
  \end{center}
  \clearpage
}%

\catcode`\@=12\relax

\endinput
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% change.cls ends here
