"""Centralized repository for all LLM prompts used in the knowledge graph system."""

# Phase 1: Main extraction prompts
MAIN_SYSTEM_PROMPT = """
You are an advanced AI system specialized in knowledge extraction and knowledge graph generation.
Your expertise includes identifying consistent entity references and meaningful relationships in text.
CRITICAL INSTRUCTION: All relationships (predicates) MUST be no more than 3 words maximum. Ideally 1-2 words. This is a hard limit.

LOCALIZATION INSTRUCTION: 
- If the input text is primarily in Chinese, output entities and predicates in Chinese.
- Use appropriate Chinese terms for concepts instead of English translations.
- Keep entities and relationships consistent with the language of the source text.
"""

MAIN_USER_PROMPT = """
Your task: Read the text below (delimited by triple backticks) and identify all Subject-Predicate-Object (S-P-O) relationships in each sentence. Then produce a single JSON array of objects, each representing one triple.

Follow these rules carefully:

- Language Consistency: Output entities and predicates in the same language as the source text. For Chinese text, use Chinese entities and predicates.
- Entity Consistency: Use consistent names for entities throughout the document. For example, if "John Smith" is mentioned as "John", "Mr. Smith", and "John Smith" in different places, use a single consistent form (preferably the most complete one) in all triples.
- Atomic Terms: Identify distinct key terms (e.g., objects, locations, organizations, acronyms, people, conditions, concepts, feelings). Avoid merging multiple ideas into one term (they should be as "atomistic" as possible).
- Unified References: Replace any pronouns (e.g., "he," "she," "it," "they," etc.) with the actual referenced entity, if identifiable.
- Pairwise Relationships: If multiple terms co-occur in the same sentence (or a short paragraph that makes them contextually related), create one triple for each pair that has a meaningful relationship.
- CRITICAL INSTRUCTION: Predicates MUST be 1-3 words maximum. Never more than 3 words. Keep them extremely concise.
- Ensure that all possible relationships are identified in the text and are captured in an S-P-O relation.
- Standardize terminology: If the same concept appears with slight variations (e.g., "artificial intelligence" and "AI"), use the most common or canonical form consistently.
- For Chinese text: Use Chinese characters for entities and predicates. Do not translate into English.
- If a person is mentioned by name, create a relation to their location, profession and what they are known for (invented, wrote, started, title, etc.) if known and if it fits the context of the information.

Important Considerations:
- Aim for precision in entity naming - use specific forms that distinguish between similar but different entities
- Maximize connectedness by using identical entity names for the same concepts throughout the document
- Consider the entire context when identifying entity references
- ALL PREDICATES MUST BE 3 WORDS OR FEWER - this is a hard requirement
- For Chinese text: Output in Chinese, maintaining natural Chinese expression

Output Requirements:

- Do not include any text or commentary outside of the JSON.
- Return only the JSON array, with each triple as an object containing "subject", "predicate", and "object".
- Make sure the JSON is valid and properly formatted.
- For Chinese text: Use Chinese characters in the JSON output.

Example of the desired output structure for Chinese text:

[
  {
    "subject": "实体A",
    "predicate": "关联",
    "object": "实体B"
  },
  {
    "subject": "实体C",
    "predicate": "使用",
    "object": "实体D"
  }
]

Example of the desired output structure for English text:

[
  {
    "subject": "Term A",
    "predicate": "relates to",
    "object": "Term B"
  },
  {
    "subject": "Term C",
    "predicate": "uses",
    "object": "Term D"
  }
]

Important: Only output the JSON array (with the S-P-O objects) and nothing else. Match the language of your output to the language of the input text.

Text to analyze (between triple backticks):
"""

# Phase 2: Entity standardization prompts
ENTITY_RESOLUTION_SYSTEM_PROMPT = """
You are an expert in entity resolution and knowledge representation.
Your task is to standardize entity names from a knowledge graph to ensure consistency.
If the entities are in Chinese, respond in Chinese. If they are in English, respond in English.
Maintain the original language of the entities.
"""

def get_entity_resolution_user_prompt(entity_list):
    # Detect if the entity list contains primarily Chinese characters
    chinese_char_count = sum(1 for char in entity_list if '\u4e00' <= char <= '\u9fff')
    total_non_space_chars = len([char for char in entity_list if not char.isspace()])
    is_chinese = chinese_char_count / max(total_non_space_chars, 1) > 0.3
    
    if is_chinese:
        return f"""
以下是从知识图谱中提取的实体名称列表。
其中一些可能指向相同的现实世界实体，但使用了不同的表述方式。

请识别指向相同概念的实体组，并为每组提供一个标准化的名称。
将您的答案以JSON对象的形式返回，其中键是标准化名称，值是应该映射到该标准名称的所有变体名称的数组。
只包含有多个变体或需要标准化的实体。

实体列表：
{entity_list}

按以下格式返回有效的JSON：
{{
  "标准化名称1": ["变体1", "变体2"],
  "标准化名称2": ["变体3", "变体4", "变体5"]
}}
"""
    else:
        return f"""
Below is a list of entity names extracted from a knowledge graph. 
Some may refer to the same real-world entities but with different wording.

Please identify groups of entities that refer to the same concept, and provide a standardized name for each group.
Return your answer as a JSON object where the keys are the standardized names and the values are arrays of all variant names that should map to that standard name.
Only include entities that have multiple variants or need standardization.

Entity list:
{entity_list}

Format your response as valid JSON like this:
{{
  "standardized name 1": ["variant 1", "variant 2"],
  "standardized name 2": ["variant 3", "variant 4", "variant 5"]
}}
"""

# Phase 3: Community relationship inference prompts
RELATIONSHIP_INFERENCE_SYSTEM_PROMPT = """
You are an expert in knowledge representation and inference. 
Your task is to infer plausible relationships between disconnected entities in a knowledge graph.
If the entities are in Chinese, respond in Chinese. If they are in English, respond in English.
Maintain the language consistency with the input entities.
"""

def get_relationship_inference_user_prompt(entities1, entities2, triples_text):
    # Detect if the input contains primarily Chinese characters
    combined_text = f"{entities1} {entities2} {triples_text}"
    chinese_char_count = sum(1 for char in combined_text if '\u4e00' <= char <= '\u9fff')
    total_non_space_chars = len([char for char in combined_text if not char.isspace()])
    is_chinese = chinese_char_count / max(total_non_space_chars, 1) > 0.3
    
    if is_chinese:
        return f"""
我有一个知识图谱，包含两个未连接的实体社区。

社区1实体：{entities1}
社区2实体：{entities2}

以下是涉及这些实体的一些现有关系：
{triples_text}

请推断社区1中的实体与社区2中的实体之间2-3个合理的关系。
以以下格式的JSON数组形式返回您的答案：

[
  {{
    "subject": "社区1中的实体",
    "predicate": "推断关系",
    "object": "社区2中的实体"
  }},
  ...
]

只包含具有明确谓词的高度合理的关系。
重要：推断的关系（谓词）必须最多3个词。最好是1-2个词。绝不超过3个词。
对于谓词，使用清楚描述关系的简短短语。
重要：确保主语和宾语是不同的实体 - 避免自我引用。
"""
    else:
        return f"""
I have a knowledge graph with two disconnected communities of entities. 

Community 1 entities: {entities1}
Community 2 entities: {entities2}

Here are some existing relationships involving these entities:
{triples_text}

Please infer 2-3 plausible relationships between entities from Community 1 and entities from Community 2.
Return your answer as a JSON array of triples in the following format:

[
  {{
    "subject": "entity from community 1",
    "predicate": "inferred relationship",
    "object": "entity from community 2"
  }},
  ...
]

Only include highly plausible relationships with clear predicates.
IMPORTANT: The inferred relationships (predicates) MUST be no more than 3 words maximum. Preferably 1-2 words. Never more than 3.
For predicates, use short phrases that clearly describe the relationship.
IMPORTANT: Make sure the subject and object are different entities - avoid self-references.
"""

# Phase 4: Within-community relationship inference prompts
WITHIN_COMMUNITY_INFERENCE_SYSTEM_PROMPT = """
You are an expert in knowledge representation and inference. 
Your task is to infer plausible relationships between semantically related entities that are not yet connected in a knowledge graph.
If the entities are in Chinese, respond in Chinese. If they are in English, respond in English.
Maintain the language consistency with the input entities.
"""

def get_within_community_inference_user_prompt(pairs_text, triples_text):
    # Detect if the input contains primarily Chinese characters
    combined_text = f"{pairs_text} {triples_text}"
    chinese_char_count = sum(1 for char in combined_text if '\u4e00' <= char <= '\u9fff')
    total_non_space_chars = len([char for char in combined_text if not char.isspace()])
    is_chinese = chinese_char_count / max(total_non_space_chars, 1) > 0.3
    
    if is_chinese:
        return f"""
我有一个知识图谱，其中包含几个在语义上相关但尚未直接连接的实体。

以下是一些可能相关的实体对：
{pairs_text}

以下是涉及这些实体的一些现有关系：
{triples_text}

请推断这些未连接实体对之间的合理关系。
以以下格式的JSON数组形式返回您的答案：

[
  {{
    "subject": "实体1",
    "predicate": "推断关系",
    "object": "实体2"
  }},
  ...
]

只包含具有明确谓词的高度合理的关系。
重要：推断的关系（谓词）必须最多3个词。最好是1-2个词。绝不超过3个词。
重要：确保主语和宾语是不同的实体 - 避免自我引用。
"""
    else:
        return f"""
I have a knowledge graph with several entities that appear to be semantically related but are not yet connected.

Here are some pairs of entities that might be related:
{pairs_text}

Here are some existing relationships involving these entities:
{triples_text}

Please infer plausible relationships between these disconnected pairs.
Return your answer as a JSON array of triples in the following format:

[
  {{
    "subject": "entity1",
    "predicate": "inferred relationship",
    "object": "entity2"
  }},
  ...
]

Only include highly plausible relationships with clear predicates.
IMPORTANT: The inferred relationships (predicates) MUST be no more than 3 words maximum. Preferably 1-2 words. Never more than 3.
IMPORTANT: Make sure that the subject and object are different entities - avoid self-references.
""" 