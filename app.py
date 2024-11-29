# import streamlit as st
# from recommend import recommend_movies
# from neo4j import GraphDatabase

# # Streamlit app
# st.title("Movie Recommendation Engine")
# watched_movie = st.text_input("Enter a movie you watched:")

# if st.button("Get Recommendations"):
#     driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
#     recommendations = recommend_movies(driver, watched_movie)
#     if recommendations:
#         st.write("You might also like:")
#         for rec in recommendations:
#             st.write(rec)
#     else:
#         st.write("No recommendations found!")



# app.py
# import streamlit as st
# from recommend import get_recommendations
# from neo4j import GraphDatabase

# # App Title
# st.title("Movie Recommendation Engine")

# # Input for watched movie
# watched_movie = st.text_input("Enter a movie you watched:")

# if st.button("Get Recommendations"):
#     driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
#     if watched_movie:
#         # Fetch recommendations
#         recommendations = get_recommendations(watched_movie)


#         if recommendations:
#             st.success("Here are some recommendations:")
#             for movie in recommendations:
#                 st.write(f"- {movie}")
                
#         else:
#             st.error("No recommendations found! Make sure the movie exists in the database.")
#     else:
#         st.error("Please enter a movie title!")


import streamlit as st
from neo4j import GraphDatabase

# Database connection function
def get_recommendations(movie_title, driver, min_recommendations=3):
    """
    Fetches movie recommendations for a given movie title.
    Ensures at least `min_recommendations` are returned, if possible.
    """
    query = f"""
    MATCH (m:Movie {{title: '{movie_title}'}})-[:SIMILAR_TO]->(recommended:Movie)
    RETURN recommended.title AS title
    LIMIT {min_recommendations}
    """
    with driver.session() as session:
        result = session.run(query)
        recommendations = [record["title"] for record in result]
        
        # Fallback logic: If fewer than required recommendations are found
        if len(recommendations) < min_recommendations:
            fallback_query = f"""
            MATCH (recommended:Movie)
            WHERE recommended.title <> '{movie_title}'
            RETURN DISTINCT recommended.title AS title
            LIMIT {min_recommendations - len(recommendations)}
            """
            fallback_result = session.run(fallback_query)
            recommendations.extend([record["title"] for record in fallback_result])
        
    return recommendations

# Streamlit App Title
st.title("Movie Recommendation Engine")

# Input for watched movie
watched_movie = st.text_input("Enter a movie you watched:")

# Get Recommendations Button
if st.button("Get Recommendations"):
    if watched_movie.strip():  # Check if input is not empty
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        
        try:
            # Fetch recommendations
            recommendations = get_recommendations(watched_movie.strip(), driver)

            if recommendations:
                st.success("Here are some recommendations:")
                for movie in recommendations:
                    st.write(f"- {movie}")
            else:
                st.error("No recommendations found! Please make sure the movie exists in the database.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            driver.close()  # Close the database connection
    else:
        st.error("Please enter a movie title!")


# import streamlit as st
# from neo4j import GraphDatabase
# import random

# # Database connection function
# def get_recommendations_with_posters(movie_title, driver, min_recommendations=3):
#     """
#     Fetches movie recommendations along with their posters.
#     Ensures at least `min_recommendations` are returned, if possible.
#     """
#     query = f"""
#     MATCH (m:Movie {{title: '{movie_title}'}})-[:SIMILAR_TO]->(recommended:Movie)
#     RETURN recommended.title AS title, recommended.poster_url AS poster
#     LIMIT {min_recommendations}
#     """
#     with driver.session() as session:
#         result = session.run(query)
#         recommendations = [{"title": record["title"], "poster": record["poster"]} for record in result]
        
#         # Fallback logic: If fewer than required recommendations are found
#         if len(recommendations) < min_recommendations:
#             fallback_query = f"""
#             MATCH (recommended:Movie)
#             WHERE recommended.title <> '{movie_title}'
#             RETURN DISTINCT recommended.title AS title, recommended.poster_url AS poster
#             LIMIT {min_recommendations - len(recommendations)}
#             """
#             fallback_result = session.run(fallback_query)
#             recommendations.extend([{"title": record["title"], "poster": record["poster"]} for record in fallback_result])
        
#     return recommendations

# # Function to fetch all movie posters for background
# def get_all_movie_posters(driver, limit=50):
#     """
#     Fetches a list of movie posters from the database for the background.
#     """
#     query = f"""
#     MATCH (m:Movie)
#     RETURN m.poster_url AS poster
#     LIMIT {limit}
#     """
#     with driver.session() as session:
#         result = session.run(query)
#         posters = [record["poster"] for record in result if record["poster"]]
#     return posters

# # Streamlit App Title
# st.markdown(
#     """
#     <style>
#     .title {
#         text-align: center;
#         font-size: 40px;
#         color: white;
#         text-shadow: 2px 2px 4px #000000;
#         margin-bottom: 20px;
#     }
#     </style>
#     <div class="title">🎬 Movie Recommendation Engine 🎥</div>
#     """,
#     unsafe_allow_html=True
# )

# # Background CSS
# def set_background(posters):
#     """
#     Creates a collage of posters in the background.
#     """
#     if posters:
#         posters_html = "".join([f"url('{poster}')" for poster in posters])
#         css = f"""
#         <style>
#         .stApp {{
#             background-image: {posters_html};
#             background-size: cover;
#             background-repeat: no-repeat;
#             background-position: center;
#         }}
#         </style>
#         """
#         st.markdown(css, unsafe_allow_html=True)

# # Input for watched movie
# watched_movie = st.text_input("Enter a movie you watched:")

# # Get Recommendations Button
# if st.button("Get Recommendations"):
#     driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    
#     try:
#         # Fetch background posters
#         all_posters = get_all_movie_posters(driver, limit=50)
#         random.shuffle(all_posters)  # Shuffle for variety
#         set_background(all_posters[:10])  # Use a subset of posters for the background

#         if watched_movie.strip():  # Check if input is not empty
#             # Fetch recommendations
#             recommendations = get_recommendations_with_posters(watched_movie.strip(), driver)

#             if recommendations:
#                 st.success("Here are some recommendations:")
#                 for movie in recommendations:
#                     st.write(f"### {movie['title']}")
#                     if movie["poster"]:
#                         st.image(movie["poster"], width=200)  # Display poster
#                     else:
#                         st.warning("Poster not available.")
#             else:
#                 st.error("No recommendations found! Please make sure the movie exists in the database.")
#         else:
#             st.error("Please enter a movie title!")
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#     finally:
#         driver.close()  # Close the database connection
